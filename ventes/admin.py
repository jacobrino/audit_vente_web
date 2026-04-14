from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Produit, Client, Vente, AuditVente
from .services import create_vente, update_vente, delete_vente


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('num_produit', 'design', 'stock', 'created_at', 'updated_at')
    search_fields = ('num_produit', 'design')
    list_filter = ('created_at', 'updated_at')
    ordering = ('num_produit',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('num_client', 'nom', 'created_at', 'updated_at')
    search_fields = ('num_client', 'nom')
    list_filter = ('created_at', 'updated_at')
    ordering = ('num_client',)


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'produit', 'qte_sortie', 'created_at', 'updated_at')
    search_fields = (
        'client__nom',
        'client__num_client',
        'produit__design',
        'produit__num_produit',
    )
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if change:
            vente = update_vente(
                vente_id=obj.pk,
                client=obj.client,
                produit=obj.produit,
                qte_sortie=obj.qte_sortie,
                utilisateur=request.user,
            )
            obj.client = vente.client
            obj.produit = vente.produit
            obj.qte_sortie = vente.qte_sortie
            obj.created_at = vente.created_at
            obj.updated_at = vente.updated_at
        else:
            vente = create_vente(
                client=obj.client,
                produit=obj.produit,
                qte_sortie=obj.qte_sortie,
                utilisateur=request.user,
            )
            obj.pk = vente.pk
            obj.client = vente.client
            obj.produit = vente.produit
            obj.qte_sortie = vente.qte_sortie
            obj.created_at = vente.created_at
            obj.updated_at = vente.updated_at

    def delete_model(self, request, obj):
        delete_vente(
            vente_id=obj.pk,
            utilisateur=request.user,
        )

    def delete_queryset(self, request, queryset):
        for vente in queryset:
            delete_vente(
                vente_id=vente.pk,
                utilisateur=request.user,
            )


@admin.register(AuditVente)
class AuditVenteAdmin(admin.ModelAdmin):
    list_display = (
        'type_operation',
        'nom_client',
        'design_produit',
        'qtesortie_ancien',
        'qtesortie_nouv',
        'utilisateur',
        'date_mise_a_jour',
    )
    search_fields = (
        'nom_client',
        'design_produit',
        'utilisateur__username',
    )
    list_filter = ('type_operation', 'date_mise_a_jour')
    ordering = ('-date_mise_a_jour',)
    readonly_fields = (
        'type_operation',
        'date_mise_a_jour',
        'nom_client',
        'design_produit',
        'qtesortie_ancien',
        'qtesortie_nouv',
        'utilisateur',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False