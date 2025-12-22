import os

from dotenv import load_dotenv
from pathlib import Path


import ssl

# Workaround SSL SOLO para entorno local (Windows / Python 3.13)
if os.environ.get('DEBUG', 'False') == 'True':
    try:
        import certifi
        ssl._create_default_https_context = lambda *args, **kwargs: ssl.create_default_context(
            cafile=certifi.where()
        )
    except ImportError:
        pass



load_dotenv()
# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-segura')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'aggregatum.com',
    'www.aggregatum.com',
    '.onrender.com',
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'contact',
    'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Debe ir justo debajo de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'aggregatum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')], 
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

WSGI_APPLICATION = 'aggregatum.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------
# CONFIGURACIÓN DE CORREO SENDGRID
# ----------------------------

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    'alexlara0956@gmail.com'  # fallback local
)

EMAIL_RECEIVER = os.environ.get(
    'EMAIL_RECEIVER',
    'alexlara0956@gmail.com'  # fallback local
)



# ----------------------------
# ARCHIVOS ESTÁTICOS
# ----------------------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Lógica Híbrida para evitar que se rompan los estilos en local
if not DEBUG:
    # En producción (Render) comprimimos y guardamos caché
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # En desarrollo usamos el almacenamiento estándar
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'



