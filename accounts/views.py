from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

from .forms import RegisterForm, ResendActivationForm


def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_path = reverse('activate', kwargs={
        'uidb64': uid,
        'token': token,
    })
    activation_url = request.build_absolute_uri(activation_path)

    resend_activation_url = request.build_absolute_uri(
        reverse('resend_activation')
    )

    subject = 'Activation de votre compte'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
        'resend_activation_url': resend_activation_url,
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        to=[user.email],
    )

    if settings.DEBUG:
        print("\n=== ACTIVATION URL ===")
        print(activation_url)
        print("======================\n")

    email = EmailMessage(
        subject=subject,
        body=message,
        to=[user.email],
    )

    email.send()


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = False
            user.save()

            send_activation_email(request, user)

            messages.success(
                request,
                "Votre compte a été créé. Un email d'activation vous a été envoyé."
            )
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès.")
        return render(request, 'accounts/activation_success.html')

    return render(request, 'accounts/activation_invalid.html')


def resend_activation_view(request):
    if request.method == 'POST':
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            user = form.user
            send_activation_email(request, user)

            messages.success(
                request,
                "Un nouvel email d'activation a été envoyé."
            )
            return redirect('login')
    else:
        form = ResendActivationForm()

    return render(request, 'accounts/resend_activation.html', {'form': form})