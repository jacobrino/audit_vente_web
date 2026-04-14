from django.urls import path
from .views import register_view, activate_account, resend_activation_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('resend-activation/', resend_activation_view, name='resend_activation'),
]