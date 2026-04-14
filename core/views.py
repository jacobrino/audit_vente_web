from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ventes.models import Produit, Client, Vente, AuditVente


@login_required
def home_view(request):
    # if request.user.is_staff or request.user.is_superuser:
    #     message = "Bienvenue en tant qu'administrateur"
    # else:
    #     message = "Bienvenue en tant qu'utilisateur normal"

    total_produits = Produit.objects.count()
    total_clients = Client.objects.count()
    total_ventes = Vente.objects.count()

    if request.user.is_superuser:
        total_insertions = AuditVente.objects.filter(
        type_operation=AuditVente.TYPE_INSERT,
        ).count()

    else :
        total_insertions = AuditVente.objects.filter(
        type_operation=AuditVente.TYPE_INSERT,
        utilisateur_id=request.user.id
        ).count()

    if request.user.is_superuser:
        total_modifications = AuditVente.objects.filter(
            type_operation=AuditVente.TYPE_UPDATE
        ).count()
    else:
        total_modifications = AuditVente.objects.filter(
            type_operation=AuditVente.TYPE_UPDATE,
            utilisateur_id=request.user.id
        ).count()


    if request.user.is_superuser:
        total_suppressions = AuditVente.objects.filter(
            type_operation=AuditVente.TYPE_DELETE
        ).count()
    else:
        total_suppressions = AuditVente.objects.filter(
            type_operation=AuditVente.TYPE_DELETE,
            utilisateur_id=request.user.id
        ).count()

    
    derniers_audits = AuditVente.objects.select_related('utilisateur')[:5]

    context = {
        'total_produits': total_produits,
        'total_clients': total_clients,
        'total_ventes': total_ventes,
        'total_insertions': total_insertions,
        'total_modifications': total_modifications,
        'total_suppressions': total_suppressions,
        'derniers_audits': derniers_audits,
    }

    return render(request, 'core/home.html', context)