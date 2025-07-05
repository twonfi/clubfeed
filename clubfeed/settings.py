from pathlib import Path
import os

from django.contrib.messages import constants as messages
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    STATIC_ROOT=(str, ""),
    MEDIA_ROOT=(str, ""),
    DB_POSTGRES_NAME=(str, ''),
    DB_POSTGRES_USER=(str, ''),
    DB_POSTGRES_PASSWORD=(str, ''),
    DB_POSTGRES_HOST=(str, ''),
    DB_POSTGRES_PORT=(str, ""),
)
Env.read_env(os.path.join(BASE_DIR, ".env"))


def _env_file(key: str) -> Path:
    env_ = env(key)

    if env_[:2] == './':
        return BASE_DIR / env_[2:]
    return Path(env_)


DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # tz_detect
    "tz_detect",
    # allauth
    "allauth_ui",
    "allauth",
    "allauth.account",
    "widget_tweaks",
    "slippers",
    # django-bootstrap5
    "django_bootstrap5",
    # django-crispy-forms
    "crispy_forms",
    "crispy_bootstrap5",
    # martor
    "martor",
    # ClubFeed
    "core",
    "creator",
    "clubs",
    "home",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    # tz_detect
    "tz_detect.middleware.TimezoneMiddleware",
    # allauth
    "allauth.account.middleware.AccountMiddleware",
    # whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "clubfeed.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                # ClubFeed
                'clubs.context_processors.can_post_context',
            ],
            "builtins": [
                "slippers.templatetags.slippers",
            ],
        },
    },
]

WSGI_APPLICATION = "clubfeed.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# POSTGRES_DATABASE = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': env('DB_POSTGRES_NAME'),
#     'USER': env('DB_POSTGRES_USER'),
#     'PASSWORD': env('DB_POSTGRES_PASSWORD'),
#     'HOST': env('DB_POSTGRES_HOST'),
#     'PORT': env('DB_POSTGRES_PORT'),
# },
#
# SQLITE_DATABASE = {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': BASE_DIR / 'db.sqlite3',
# },

match env('DATABASE'):
    case 'sqlite':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            },
        }
    case 'postgres':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': env('DB_POSTGRES_NAME'),
                'USER': env('DB_POSTGRES_USER'),
                'PASSWORD': env('DB_POSTGRES_PASSWORD'),
                'HOST': env('DB_POSTGRES_HOST'),
                'PORT': env('DB_POSTGRES_PORT'),
            },
        }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) and media files
# https://docs.djangoproject.com/en/5.2/howto/static-files/

if DEBUG:
    STATIC_URL = "static/"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    STATIC_URL = env("STATIC_URL")
    STATIC_ROOT = _env_file("STATIC_ROOT")

    MEDIA_URL = env("MEDIA_URL")
    MEDIA_ROOT = _env_file("MEDIA_ROOT")

    STATICFILES_STORAGE = ('whitenoise.'
                           'storage.CompressedManifestStaticFilesStorage')

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# allauth
ACCOUNT_ADAPTER = 'users.allauth.AccountAdapter'

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Bootstrap message tags
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# martor
MARTOR_THEME = "bootstrap"
MARTOR_ENABLE_ADMIN_CSS = False
MARTOR_TOOLBAR_BUTTONS = [
    "bold",
    "italic",
    "horizontal",
    "heading",
    "pre-code",
    "blockquote",
    "unordered-list",
    "ordered-list",
    "link",
    "image-link",
    # 'emoji',  # until dependency hell with pymdownx is fixed
    "direct-mention",
    "toggle-maximize",
    "help",
]
MARTOR_ALTERNATIVE_JS_FILE_THEME = 'martor/martor.js'
MARTOR_ALTERNATIVE_CSS_FILE_THEME = 'martor/martor.css'
