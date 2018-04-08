"""
Django settings for busfit project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from os.path import abspath, dirname, join, exists
import json

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy as _r


# Build paths inside the Django project like this: join(BASE_DIR, "directory_or_file")
# `BASE_DIR` is taken as the `src` folder that lives at the root.
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
# `PROJECT_DIR` is the root of the repository.
PROJECT_DIR = dirname(BASE_DIR)
STATIC_ROOT = join(BASE_DIR, 'staticroot')
STATICFILES_DIRS = [join(BASE_DIR, 'static')]
MEDIA_ROOT = join(BASE_DIR, 'mediaroot')
MEDIA_URL = "/media/"


# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "busfit.context_processors.business",
                "busfit.context_processors.theme",
            ],
        },
    },
]


# Use 12factor inspired environment variables or from a file
import environ
env = environ.Env()

# Ideally env file should be outside the git repo
# i.e. PROJECT_DIR.parent
env_files = [join(dirname(PROJECT_DIR), 'local.env'), join(PROJECT_DIR, 'local.env')]
for env_file in env_files:
	if exists(env_file):
		print('Env File Detected')
		environ.Env.read_env(str(env_file))
		break
	else:
		print('No Env File')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('BUSFIT_SECRET_KEY', default=env('SECRET_KEY'))

# Admins
ADMINS = (('konoufo', 'konoufo1@gmail.com'),)
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
with open(join(PROJECT_DIR, 'config.json'), 'r') as f:
	INSTALLED_APPS += json.loads(f.read()).get('django_apps', [])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'busfit.middleware.AjaxRedirectMiddleware',
]

ROOT_URLCONF = 'busfit.urls'

WSGI_APPLICATION = 'busfit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

SITE_ID = 1


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'


LOCALE_PATHS = (join(BASE_DIR, 'locale'), )

LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': join(PROJECT_DIR, 'webpack-stats.json')
    }
}

# Crispy Form Theme - Bootstrap 3
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Authentication Settings
AUTH_USER_MODEL = 'authtools.User'
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_URL = _r("account_login")
LOGIN_URL = _r("account_login")
ACCOUNT_SIGNUP_REDIRECT_URL = ACCOUNT_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL = _r("profiles:show_self")
ACCOUNT_LOGOUT_REDIRECT_URL = _r("home")
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

AUTHENTICATION_BACKENDS = [
    "social.backends.twitter.TwitterOAuth",
    "account.auth_backends.EmailAuthenticationBackend",
]

SOCIAL_AUTH_TWITTER_KEY = ""
SOCIAL_AUTH_TWITTER_SECRET = ""


# Stripe API - Payment Aggregator
# usage: stripe.api_key = STRIPE_API_KEY

STRIPE_API_KEY = env('BUSFIT_STRIPE_API', default='')


THUMBNAIL_EXTENSION = 'png'     # Or any extn for your thumbnails
