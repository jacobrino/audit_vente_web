from django.urls import path
from . import views

urlpatterns = [
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/ajouter/', views.produit_create, name='produit_create'),
    path('produits/<int:pk>/modifier/', views.produit_update, name='produit_update'),
    path('produits/<int:pk>/supprimer/', views.produit_delete, name='produit_delete'),

    path('clients/', views.client_list, name='client_list'),
    path('clients/ajouter/', views.client_create, name='client_create'),
    path('clients/<int:pk>/modifier/', views.client_update, name='client_update'),
    path('clients/<int:pk>/supprimer/', views.client_delete, name='client_delete'),

    path('ventes/', views.vente_list, name='vente_list'),
    path('ventes/ajouter/', views.vente_create, name='vente_create'),
    path('ventes/<int:pk>/modifier/', views.vente_update, name='vente_update'),
    path('ventes/<int:pk>/supprimer/', views.vente_delete, name='vente_delete'),

    path('audits/', views.audit_list, name='audit_list'),
]