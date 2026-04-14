from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Produit, Vente, AuditVente


def create_vente(*, client, produit, qte_sortie, utilisateur=None):
    if qte_sortie <= 0:
        raise ValidationError("La quantité sortie doit être supérieure à 0.")

    with transaction.atomic():
        produit_locked = Produit.objects.select_for_update().get(pk=produit.pk)

        if produit_locked.stock < qte_sortie:
            raise ValidationError(
                f"Stock insuffisant pour le produit '{produit_locked.design}'. "
                f"Stock disponible : {produit_locked.stock}, quantité demandée : {qte_sortie}."
            )

        produit_locked.stock -= qte_sortie
        produit_locked.save()

        vente = Vente.objects.create(
            client=client,
            produit=produit_locked,
            qte_sortie=qte_sortie,
        )

        AuditVente.objects.create(
            type_operation=AuditVente.TYPE_INSERT,
            nom_client=client.nom,
            design_produit=produit_locked.design,
            qtesortie_ancien=None,
            qtesortie_nouv=qte_sortie,
            utilisateur=utilisateur,
        )

        return vente


def update_vente(*, vente_id, client, produit, qte_sortie, utilisateur=None):
    if qte_sortie <= 0:
        raise ValidationError("La quantité sortie doit être supérieure à 0.")

    with transaction.atomic():
        vente = Vente.objects.select_for_update().select_related('produit', 'client').get(pk=vente_id)

        ancien_client = vente.client
        ancien_produit = vente.produit
        ancienne_qte = vente.qte_sortie

        product_ids = sorted({ancien_produit.pk, produit.pk})
        produits_locked = {
            p.pk: p
            for p in Produit.objects.select_for_update().filter(pk__in=product_ids)
        }

        ancien_produit_locked = produits_locked[ancien_produit.pk]
        nouveau_produit_locked = produits_locked[produit.pk]

        if ancien_produit_locked.pk == nouveau_produit_locked.pk:
            stock_disponible_apres_restitution = ancien_produit_locked.stock + ancienne_qte

            if stock_disponible_apres_restitution < qte_sortie:
                raise ValidationError(
                    f"Stock insuffisant pour le produit '{ancien_produit_locked.design}'. "
                    f"Stock disponible après restitution : {stock_disponible_apres_restitution}, "
                    f"quantité demandée : {qte_sortie}."
                )

            ancien_produit_locked.stock = stock_disponible_apres_restitution - qte_sortie
            ancien_produit_locked.save()

        else:
            ancien_produit_locked.stock += ancienne_qte
            ancien_produit_locked.save()

            if nouveau_produit_locked.stock < qte_sortie:
                raise ValidationError(
                    f"Stock insuffisant pour le produit '{nouveau_produit_locked.design}'. "
                    f"Stock disponible : {nouveau_produit_locked.stock}, quantité demandée : {qte_sortie}."
                )

            nouveau_produit_locked.stock -= qte_sortie
            nouveau_produit_locked.save()

        vente.client = client
        vente.produit = nouveau_produit_locked
        vente.qte_sortie = qte_sortie
        vente.save()

        AuditVente.objects.create(
            type_operation=AuditVente.TYPE_UPDATE,
            nom_client=client.nom,
            design_produit=nouveau_produit_locked.design,
            qtesortie_ancien=ancienne_qte,
            qtesortie_nouv=qte_sortie,
            utilisateur=utilisateur,
        )

        return vente


def delete_vente(*, vente_id, utilisateur=None):
    with transaction.atomic():
        vente = Vente.objects.select_for_update().select_related('produit', 'client').get(pk=vente_id)
        produit_locked = Produit.objects.select_for_update().get(pk=vente.produit.pk)

        ancienne_qte = vente.qte_sortie
        nom_client = vente.client.nom
        design_produit = produit_locked.design

        produit_locked.stock += ancienne_qte
        produit_locked.save()

        AuditVente.objects.create(
            type_operation=AuditVente.TYPE_DELETE,
            nom_client=nom_client,
            design_produit=design_produit,
            qtesortie_ancien=ancienne_qte,
            qtesortie_nouv=None,
            utilisateur=utilisateur,
        )

        vente.delete()