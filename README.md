# Audit Vente Web

Application web de gestion et d’audit des ventes développée avec **Django**, **Bootstrap**, **Font Awesome** et **MySQL**.

## Fonctionnalités principales

L’application permet de :

- gérer les **produits**
- gérer les **clients**
- gérer les **ventes**
- mettre à jour automatiquement le **stock**
- enregistrer un **audit des opérations** sur les ventes
- afficher un **tableau de bord** avec statistiques
- gérer l’authentification avec :
  - inscription
  - connexion
  - activation de compte par email
  - renvoi du lien d’activation

## Stack technique

- **Backend** : Django
- **Frontend** : Bootstrap 5 + Font Awesome
- **Base de données** : MySQL
- **Email** : SMTP ou backend console/filebased selon l’environnement

---

## 1. Prérequis

Avant de lancer le projet, il faut installer :

- Python 3
- pip
- venv
- MySQL Server
- Git

Sous Ubuntu/Debian :

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv mysql-server git pkg-config build-essential python3-dev default-libmysqlclient-dev
```

---

## 2. Cloner le projet

```bash
git clone <url-du-projet>
cd audit_vente_web
```

---

## 3. Créer et activer l’environnement virtuel

Sous Linux/macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

Sous Windows :

```bash
venv\Scripts\activate
```

---

## 4. Installer les dépendances

Si le fichier `requirements.txt` est déjà présent :

```bash
pip install -r requirements.txt
```

Sinon, au minimum :

```bash
pip install django mysqlclient python-dotenv
```

---

## 5. Créer la base de données MySQL

Connexion à MySQL :

```bash
mysql -u root -p
```

Puis création de la base :

```sql
CREATE DATABASE audit_vente_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 6. Créer le fichier `.env`

À la racine du projet, créer un fichier `.env`.

### Exemple avec SMTP Gmail

```env
DB_NAME=audit_vente_db
DB_USER=root
DB_PASSWORD=ton_mot_de_passe_mysql
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tonadresse@gmail.com
EMAIL_HOST_PASSWORD=ton_mot_de_passe_application
DEFAULT_FROM_EMAIL=tonadresse@gmail.com
```

### Exemple pour test local sans email réel

```env
DB_NAME=audit_vente_db
DB_USER=root
DB_PASSWORD=ton_mot_de_passe_mysql
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@auditvente.com
```

---

## 7. Vérifier la configuration Django

Le fichier `config/settings.py` doit :

- lire les variables du `.env`
- utiliser MySQL
- inclure les apps :
  - `accounts`
  - `core`
  - `ventes`

Exemple de configuration pour la base de données :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

---

## 8. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 9. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

---

## 10. Charger les utilisateurs de test

```bash
python manage.py seed_users
```

---

## 11. Charger les données métier

```bash
python manage.py seed_business_data --reset
```

Cette commande insère des données cohérentes de démonstration :

- produits
- clients
- ventes
- audits

---

## 12. Lancer le serveur

```bash
python manage.py runserver
```

Puis ouvrir :

```text
http://127.0.0.1:8000/
```

---

## 13. Routes principales

### Authentification

- `/accounts/register/`
- `/accounts/login/`
- `/accounts/resend-activation/`

### Application

- `/`
- `/produits/`
- `/clients/`
- `/ventes/`
- `/audits/`

### Administration

- `/admin/`

---

## 14. Rôles et permissions

### Administrateur

Peut :

- gérer les produits
- gérer les clients
- gérer les ventes
- supprimer les ventes
- consulter les audits
- accéder à l’administration Django

### Utilisateur normal

Peut :

- consulter les produits
- consulter les clients
- consulter les ventes
- ajouter une vente
- modifier une vente
- consulter le tableau de bord

Ne peut pas :

- modifier les produits
- modifier les clients
- supprimer une vente
- consulter l’audit global

---

## 15. Logique métier

L’application met en œuvre la logique suivante :

### Création d’une vente

- vérifie le stock disponible
- décrémente le stock
- crée un audit `INSERT`

### Modification d’une vente

- ajuste le stock selon l’ancienne et la nouvelle quantité
- crée un audit `UPDATE`

### Suppression d’une vente

- restitue la quantité au stock
- crée un audit `DELETE`

---

## 16. Tableau de bord

La page d’accueil affiche :

- le message de bienvenue selon le rôle
- le nombre total de produits
- le nombre total de clients
- le nombre total de ventes
- le nombre total :
  - d’insertions
  - de modifications
  - de suppressions
- les dernières opérations d’audit

---

## 17. Pagination

Une pagination est active sur les listes :

- produits
- clients
- ventes
- audits

---

## 18. Structure du projet

```text
audit_vente_web/
├── accounts/
├── core/
├── ventes/
├── config/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## 19. Commandes utiles

### Lancer le projet

```bash
python manage.py runserver
```

### Faire les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Créer un superuser

```bash
python manage.py createsuperuser
```

### Seeder les utilisateurs

```bash
python manage.py seed_users
```

### Seeder les données métier

```bash
python manage.py seed_business_data --reset
```

---

## 20. Vérifications recommandées

Après installation, vérifier :

- la connexion avec un compte admin
- la connexion avec un compte utilisateur normal
- l’ajout d’une vente
- la mise à jour automatique du stock
- la création de l’audit
- les restrictions d’accès selon le rôle
- la pagination des listes
- l’envoi d’email d’activation si SMTP activé

---

## 21. Problèmes fréquents

### `mysqlclient` ne s’installe pas

Sous Ubuntu :

```bash
sudo apt install -y pkg-config build-essential python3-dev default-libmysqlclient-dev
pip install mysqlclient
```

### Erreur de connexion MySQL

Vérifier :

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

### Email non envoyé

Vérifier :

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

---

## 22. Fichiers importants à ne pas oublier

- `requirements.txt`
- `.env.example`
- `.gitignore`
- `README.md`

---

## 23. Séquence rapide d’installation

```bash
git clone <url-du-projet>
cd audit_vente_web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_users
python manage.py seed_business_data --reset
python manage.py runserver
```

Puis ouvrir :

```text
http://127.0.0.1:8000/
```

---

## Auteur

Projet réalisé avec Django, Bootstrap et MySQL pour la gestion et l’audit des ventes.