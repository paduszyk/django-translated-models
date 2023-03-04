from pathlib import Path

# Paths

PROJECT_DIR = Path(__file__).resolve().parent

BASE_DIR = PROJECT_DIR.parent


# Secret key

SECRET_KEY = "secret-key"


# Debugging

DEBUG = True


# Allowed hosts

ALLOWED_HOSTS = ["*"]


# Databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# Apps

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "translated_models",
]


# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLconf

ROOT_URLCONF = "tests.urls"


# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Internationalization

USE_TZ = True

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

LANGUAGES = [("en", "English"), ("pl", "Polish")]


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
