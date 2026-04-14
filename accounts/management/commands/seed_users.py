# accounts/management/commands/seed_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Créer 2 admins et 2 utilisateurs normaux'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                'username': 'admin1',
                'first_name': 'Admin',
                'last_name': 'One',
                'email': 'admin1@example.com',
                'password': 'Admin12345',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'admin2',
                'first_name': 'Admin',
                'last_name': 'Two',
                'email': 'admin2@example.com',
                'password': 'Admin12345',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'user1',
                'first_name': 'User',
                'last_name': 'One',
                'email': 'user1@example.com',
                'password': 'User12345',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'user2',
                'first_name': 'User',
                'last_name': 'Two',
                'email': 'user2@example.com',
                'password': 'User12345',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        for data in users_data:
            username = data['username']

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'],
                )
                user.is_staff = data['is_staff']
                user.is_superuser = data['is_superuser']
                user.is_active = True
                user.save()

                self.stdout.write(self.style.SUCCESS(f'Utilisateur créé : {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Utilisateur existe déjà : {username}'))