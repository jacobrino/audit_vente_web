from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_required
from .forms import ProduitForm, ClientForm, VenteForm
from .models import Produit, Client, Vente, AuditVente
from .services import create_vente, update_vente, delete_vente


# =========================
# PRODUITS
# =========================

@login_required
def produit_list(request):
    produits_qs = Produit.objects.all().order_by('num_produit')
    paginator = Paginator(produits_qs, 10)
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, 'ventes/produit_list.html', {'produits': produits})


@login_required
@admin_required
def produit_create(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit ajouté avec succès.")
            return redirect('produit_list')
    else:
        form = ProduitForm()

    return render(request, 'ventes/produit_form.html', {
        'form': form,
        'title': 'Ajouter un produit',
        'button_text': 'Enregistrer',
    })


@login_required
@admin_required
def produit_update(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès.")
            return redirect('produit_list')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'ventes/produit_form.html', {
        'form': form,
        'title': 'Modifier un produit',
        'button_text': 'Mettre à jour',
    })


@login_required
@admin_required
def produit_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Produit supprimé avec succès.")
        return redirect('produit_list')

    return render(request, 'ventes/produit_confirm_delete.html', {'produit': produit})


# =========================
# CLIENTS
# =========================

@login_required
def client_list(request):
    clients_qs = Client.objects.all().order_by('num_client')
    paginator = Paginator(clients_qs, 10)
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)

    return render(request, 'ventes/client_list.html', {'clients': clients})


@login_required
@admin_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client ajouté avec succès.")
            return redirect('client_list')
    else:
        form = ClientForm()

    return render(request, 'ventes/client_form.html', {
        'form': form,
        'title': 'Ajouter un client',
        'button_text': 'Enregistrer',
    })


@login_required
@admin_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client modifié avec succès.")
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'ventes/client_form.html', {
        'form': form,
        'title': 'Modifier un client',
        'button_text': 'Mettre à jour',
    })


@login_required
@admin_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client supprimé avec succès.")
        return redirect('client_list')

    return render(request, 'ventes/client_confirm_delete.html', {'client': client})


# =========================
# VENTES
# =========================

@login_required
def vente_list(request):
    ventes_qs = Vente.objects.select_related('client', 'produit').all().order_by('-created_at')
    paginator = Paginator(ventes_qs, 10)
    page_number = request.GET.get('page')
    ventes = paginator.get_page(page_number)

    return render(request, 'ventes/vente_list.html', {'ventes': ventes})


@login_required
def vente_create(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            try:
                create_vente(
                    client=form.cleaned_data['client'],
                    produit=form.cleaned_data['produit'],
                    qte_sortie=form.cleaned_data['qte_sortie'],
                    utilisateur=request.user,
                )
                messages.success(request, "Vente ajoutée avec succès.")
                return redirect('vente_list')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = VenteForm()

    return render(request, 'ventes/vente_form.html', {
        'form': form,
        'title': 'Ajouter une vente',
        'button_text': 'Enregistrer',
    })


@login_required
def vente_update(request, pk):
    vente = get_object_or_404(Vente, pk=pk)

    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            try:
                update_vente(
                    vente_id=vente.pk,
                    client=form.cleaned_data['client'],
                    produit=form.cleaned_data['produit'],
                    qte_sortie=form.cleaned_data['qte_sortie'],
                    utilisateur=request.user,
                )
                messages.success(request, "Vente modifiée avec succès.")
                return redirect('vente_list')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = VenteForm(instance=vente)

    return render(request, 'ventes/vente_form.html', {
        'form': form,
        'title': 'Modifier une vente',
        'button_text': 'Mettre à jour',
    })


@login_required
@admin_required
def vente_delete(request, pk):
    vente = get_object_or_404(Vente.objects.select_related('client', 'produit'), pk=pk)

    if request.method == 'POST':
        try:
            delete_vente(
                vente_id=vente.pk,
                utilisateur=request.user,
            )
            messages.success(request, "Vente supprimée avec succès.")
            return redirect('vente_list')
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('vente_list')

    return render(request, 'ventes/vente_confirm_delete.html', {'vente': vente})


# =========================
# AUDIT
# =========================

@login_required
@admin_required
def audit_list(request):
    audits_qs = AuditVente.objects.select_related('utilisateur').all().order_by('-date_mise_a_jour')
    paginator = Paginator(audits_qs, 10)
    page_number = request.GET.get('page')
    audits = paginator.get_page(page_number)

    return render(request, 'ventes/audit_list.html', {'audits': audits})