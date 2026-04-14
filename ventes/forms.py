from django import forms
from django.core.exceptions import ValidationError

from .models import Produit, Client, Vente


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['num_produit', 'design', 'stock']
        widgets = {
            'num_produit': forms.TextInput(attrs={'class': 'form-control'}),
            'design': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['num_client', 'nom']
        widgets = {
            'num_client': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['client', 'produit', 'qte_sortie']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'qte_sortie': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_qte_sortie(self):
        qte_sortie = self.cleaned_data.get('qte_sortie')

        if qte_sortie is None or qte_sortie <= 0:
            raise ValidationError("La quantité sortie doit être supérieure à 0.")

        return qte_sortie