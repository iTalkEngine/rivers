"""
Settings globales de Rivers.
Personnalisables en surchargeant un fichier externe.
"""

DEBUG = True
SECRET_KEY = "rivers-secret-key"
ALLOWED_HOSTS = ["*"]

# Database placeholder
DATABASES = {
    "default": {
        "ENGINE": "sqlite",
        "NAME": "rivers.db"
    }
}

# Middleware par défaut (ordre pro)
MIDDLEWARE = [
    "security",
    "logging",
    "auth",
]

# Autres settings
APP_NAME = "Rivers"
VERSION = "0.1.0"
