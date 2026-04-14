from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-f3e*-3cv2dhy22njvnl3dt8ia&04i8m1+&#p&=p^v5i)o_##m6'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'accounts',
    'core',
    'ventes',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'audit_vente_db',
        'USER': 'phpmyadmin',
        'PASSWORD': '0000',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Indian/Antananarivo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Authentication redirects
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Email configuration
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#Contenu Email envoyé sous forme fichier enregistré dans le dossier /sent_emails
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#Contenu Email envoyé dans le console du serveur 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = int(587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jacobrino05@gmail.com"
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "jacobrino05@gmail.com"
MAIL_FROM_NAME="Audit vente"

# DEFAULT_FROM_EMAIL = 'no-reply@auditvente.com'


PASSWORD_RESET_TIMEOUT = 604800  # 7 jours

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'