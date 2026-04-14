from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from ventes.models import Produit, Client, Vente, AuditVente
from ventes.services import create_vente


class Command(BaseCommand):
    help = "Insère 50 produits, 50 clients et 50 ventes cohérentes"

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprime les données métier existantes avant de reseeder.'
        )

    def handle(self, *args, **options):
        reset = options['reset']

        with transaction.atomic():
            if reset:
                self.stdout.write(self.style.WARNING("Réinitialisation des données métier..."))
                AuditVente.objects.all().delete()
                Vente.objects.all().delete()
                Client.objects.all().delete()
                Produit.objects.all().delete()

            produits = self.seed_produits()
            clients = self.seed_clients()
            self.seed_ventes(produits, clients)

        self.stdout.write(self.style.SUCCESS("Seed métier terminé avec succès."))

    def seed_produits(self):
        produits_data = [
            ("P001", "Ordinateur portable 15 pouces", 30),
            ("P002", "Ordinateur portable 14 pouces", 25),
            ("P003", "Écran LED 24 pouces", 20),
            ("P004", "Écran LED 27 pouces", 18),
            ("P005", "Souris USB filaire", 80),
            ("P006", "Souris sans fil", 60),
            ("P007", "Clavier bureautique AZERTY", 45),
            ("P008", "Clavier mécanique RGB", 35),
            ("P009", "Casque audio USB", 40),
            ("P010", "Micro-casque professionnel", 28),
            ("P011", "Imprimante laser monochrome", 15),
            ("P012", "Imprimante multifonction couleur", 12),
            ("P013", "Disque SSD 256 Go", 50),
            ("P014", "Disque SSD 512 Go", 45),
            ("P015", "Disque dur externe 1 To", 38),
            ("P016", "Disque dur externe 2 To", 30),
            ("P017", "Clé USB 32 Go", 100),
            ("P018", "Clé USB 64 Go", 90),
            ("P019", "Routeur Wi-Fi double bande", 22),
            ("P020", "Switch réseau 8 ports", 24),
            ("P021", "Switch réseau 24 ports", 10),
            ("P022", "Onduleur 650 VA", 16),
            ("P023", "Onduleur 1200 VA", 12),
            ("P024", "Webcam HD", 34),
            ("P025", "Webcam Full HD", 26),
            ("P026", "Projecteur HDMI", 8),
            ("P027", "Support écran réglable", 20),
            ("P028", "Station d'accueil USB-C", 18),
            ("P029", "Câble HDMI 2 mètres", 120),
            ("P030", "Câble réseau RJ45 5 mètres", 140),
            ("P031", "Chargeur universel PC", 20),
            ("P032", "Tablette 10 pouces", 17),
            ("P033", "Téléphone IP bureautique", 25),
            ("P034", "Caméra de surveillance IP", 14),
            ("P035", "Batterie externe 10000 mAh", 36),
            ("P036", "Batterie externe 20000 mAh", 24),
            ("P037", "Enceinte Bluetooth portable", 32),
            ("P038", "Scanner de documents", 11),
            ("P039", "Lecteur code-barres USB", 29),
            ("P040", "Étiquetteuse thermique", 13),
            ("P041", "Point d'accès Wi-Fi", 15),
            ("P042", "Mini PC bureautique", 19),
            ("P043", "Mémoire RAM 8 Go DDR4", 42),
            ("P044", "Mémoire RAM 16 Go DDR4", 35),
            ("P045", "Carte microSD 64 Go", 75),
            ("P046", "Adaptateur USB vers Ethernet", 33),
            ("P047", "Hub USB 4 ports", 40),
            ("P048", "Lampe de bureau LED", 27),
            ("P049", "Chaise de bureau ergonomique", 9),
            ("P050", "Bureau informatique compact", 7),
        ]

        produits = []

        for num_produit, design, stock in produits_data:
            produit, created = Produit.objects.get_or_create(
                num_produit=num_produit,
                defaults={
                    'design': design,
                    'stock': stock,
                }
            )

            if not created:
                produit.design = design
                if not Vente.objects.filter(produit=produit).exists():
                    produit.stock = stock
                produit.save()

            produits.append(produit)

        self.stdout.write(self.style.SUCCESS(f"{len(produits)} produits prêts."))
        return produits

    def seed_clients(self):
        clients_data = [
            ("C001", "Rakoto Jean"),
            ("C002", "Rabe Marie"),
            ("C003", "Andrianina Paul"),
            ("C004", "Randria Sophie"),
            ("C005", "Rasoa Clarisse"),
            ("C006", "Razafindrakoto Eric"),
            ("C007", "Raveloson Hery"),
            ("C008", "Ratsimba Nadia"),
            ("C009", "Razanamihaja Tiana"),
            ("C010", "Randriamifidisoa Fara"),
            ("C011", "Raharison Luc"),
            ("C012", "Rafanomezantsoa Mialy"),
            ("C013", "Rabearivelo Toky"),
            ("C014", "Rajaonarivony Aina"),
            ("C015", "Ramaroson Julio"),
            ("C016", "Rasoanirina Vola"),
            ("C017", "Rakotondrazaka Hanta"),
            ("C018", "Ratsiraka Nomena"),
            ("C019", "Rasolofonirina Tahina"),
            ("C020", "Ramiandrisoa Elodie"),
            ("C021", "Ravelomanantsoa Kanto"),
            ("C022", "Rabenja Mamy"),
            ("C023", "Razafimahefa Joël"),
            ("C024", "Randrianasolo Miora"),
            ("C025", "Rakotomalala Thierry"),
            ("C026", "Ravalitera Fenosoa"),
            ("C027", "Rafaralahy Patrick"),
            ("C028", "Razanajatovo Hanitra"),
            ("C029", "Ratsimbazafy Lova"),
            ("C030", "Ramanantsoa Hoby"),
            ("C031", "Raharimalala Cedric"),
            ("C032", "Razafimamonjy Lantosoa"),
            ("C033", "Rabetsimialona Tojo"),
            ("C034", "Rajoelison Fitia"),
            ("C035", "Rafidinarivo Angelo"),
            ("C036", "Ramilison Noro"),
            ("C037", "Rasendrasoa Kevin"),
            ("C038", "Randriatsiferana Vero"),
            ("C039", "Rabezandrina Mahefa"),
            ("C040", "Ramanitra Olivia"),
            ("C041", "Rafalimanana Mika"),
            ("C042", "Rabenoro Sarah"),
            ("C043", "Razakamiadana Liva"),
            ("C044", "Ratsimbason Aro"),
            ("C045", "Ratsara Harena"),
            ("C046", "Ravelona Onja"),
            ("C047", "Rafanomezana Prisca"),
            ("C048", "Rasoazanany Haja"),
            ("C049", "Razafintsalama Dino"),
            ("C050", "Rabekoto Niry"),
        ]

        clients = []

        for num_client, nom in clients_data:
            client, created = Client.objects.get_or_create(
                num_client=num_client,
                defaults={'nom': nom}
            )

            if not created:
                client.nom = nom
                client.save()

            clients.append(client)

        self.stdout.write(self.style.SUCCESS(f"{len(clients)} clients prêts."))
        return clients

    def seed_ventes(self, produits, clients):
        if Vente.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Des ventes existent déjà. Le seeder n'ajoute pas de nouvelles ventes sans --reset."
                )
            )
            return

        user = (
            User.objects.filter(is_superuser=True).first()
            or User.objects.filter(is_staff=True).first()
            or User.objects.first()
        )

        ventes_data = [
            ("C001", "P005", 5),
            ("C002", "P006", 3),
            ("C003", "P007", 4),
            ("C004", "P008", 2),
            ("C005", "P009", 3),
            ("C006", "P010", 2),
            ("C007", "P013", 4),
            ("C008", "P014", 2),
            ("C009", "P017", 10),
            ("C010", "P018", 8),
            ("C011", "P019", 2),
            ("C012", "P020", 2),
            ("C013", "P022", 1),
            ("C014", "P024", 3),
            ("C015", "P025", 2),
            ("C016", "P027", 2),
            ("C017", "P028", 1),
            ("C018", "P029", 12),
            ("C019", "P030", 15),
            ("C020", "P031", 2),
            ("C021", "P032", 1),
            ("C022", "P033", 3),
            ("C023", "P035", 4),
            ("C024", "P036", 2),
            ("C025", "P037", 3),
            ("C026", "P038", 1),
            ("C027", "P039", 4),
            ("C028", "P040", 1),
            ("C029", "P041", 2),
            ("C030", "P042", 1),
            ("C031", "P043", 6),
            ("C032", "P044", 4),
            ("C033", "P045", 10),
            ("C034", "P046", 3),
            ("C035", "P047", 5),
            ("C036", "P048", 2),
            ("C037", "P003", 2),
            ("C038", "P004", 1),
            ("C039", "P011", 1),
            ("C040", "P012", 1),
            ("C041", "P015", 2),
            ("C042", "P016", 1),
            ("C043", "P021", 1),
            ("C044", "P023", 1),
            ("C045", "P026", 1),
            ("C046", "P034", 1),
            ("C047", "P049", 1),
            ("C048", "P050", 1),
            ("C049", "P001", 2),
            ("C050", "P002", 2),
        ]

        clients_map = {client.num_client: client for client in clients}
        produits_map = {produit.num_produit: produit for produit in produits}

        created_count = 0

        for num_client, num_produit, qte_sortie in ventes_data:
            client = clients_map[num_client]
            produit = produits_map[num_produit]

            create_vente(
                client=client,
                produit=produit,
                qte_sortie=qte_sortie,
                utilisateur=user,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} ventes créées."))
        self.stdout.write(self.style.SUCCESS(f"{created_count} audits INSERT générés automatiquement."))


# Commande pour les exécuter "python manage.py seed_business_data"