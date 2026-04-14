from django.db import models
from django.contrib.auth.models import User


class Produit(models.Model):
    num_produit = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro produit"
    )
    design = models.CharField(
        max_length=255,
        verbose_name="Désignation"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['num_produit']

    def __str__(self):
        return f"{self.num_produit} - {self.design}"


class Client(models.Model):
    num_client = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro client"
    )
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du client"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['num_client']

    def __str__(self):
        return f"{self.num_client} - {self.nom}"


class Vente(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='ventes',
        verbose_name="Client"
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='ventes',
        verbose_name="Produit"
    )
    qte_sortie = models.PositiveIntegerField(
        verbose_name="Quantité sortie"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(qte_sortie__gt=0),
                name='vente_qte_sortie_gt_0'
            )
        ]

    def __str__(self):
        return f"Vente #{self.id} - {self.client.nom} - {self.produit.design} - {self.qte_sortie}"


class AuditVente(models.Model):
    TYPE_INSERT = 'INSERT'
    TYPE_UPDATE = 'UPDATE'
    TYPE_DELETE = 'DELETE'

    TYPE_OPERATION_CHOICES = [
        (TYPE_INSERT, 'Insertion'),
        (TYPE_UPDATE, 'Modification'),
        (TYPE_DELETE, 'Suppression'),
    ]

    type_operation = models.CharField(
        max_length=10,
        choices=TYPE_OPERATION_CHOICES,
        verbose_name="Type d'opération"
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de mise à jour"
    )
    nom_client = models.CharField(
        max_length=255,
        verbose_name="Nom du client"
    )
    design_produit = models.CharField(
        max_length=255,
        verbose_name="Désignation du produit"
    )
    qtesortie_ancien = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Ancienne quantité sortie"
    )
    qtesortie_nouv = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Nouvelle quantité sortie"
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Utilisateur"
    )

    class Meta:
        verbose_name = "Audit de vente"
        verbose_name_plural = "Audit des ventes"
        ordering = ['-date_mise_a_jour']

    def __str__(self):
        return f"{self.type_operation} - {self.nom_client} - {self.design_produit} - {self.date_mise_a_jour:%d/%m/%Y %H:%M}"