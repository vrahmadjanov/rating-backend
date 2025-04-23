from pathlib import Path
import os
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials

# ==================================================
# Базовые настройки проекта
# ==================================================

# Путь к базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django (используется для шифрования)
SECRET_KEY = os.getenv('SECRET_KEY')

# Режим отладки (включать только в разработке)
DEBUG = os.getenv('DEBUG')

# Разрешенные хосты (для безопасности)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Настройки CORS (разрешенные источники для запросов)
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://89.111.172.86:3000').split(',')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Стандартный бэкенд для админки
    'core.backends.PhoneNumberBackend',  # Ваш кастомный бэкенд
]

# ==================================================
# Настройки Firebase
# ==================================================

# Путь к файлу с учетными данными Firebase
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "samt-backend-firebase-adminsdk-fbsvc-27e8558347.json")

# Инициализация Firebase, если еще не инициализирован
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

# ==================================================
# Установленные приложения
# ==================================================

INSTALLED_APPS = [
    # Стандартные приложения Django
    'modeltranslation',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние приложения
    'storages',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'fcm_django',

    # Пользовательские приложения
    'a_base',
    'subscriptions',
    'core',
    'doctors',
    'appointments',
    'patients',
    'notifications',
    'ehr',
    'chat',
]

ASGI_APPLICATION = 'rating.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Модель пользователя по умолчанию
AUTH_USER_MODEL = "core.CustomUser"

# Настройки FCM (Firebase Cloud Messaging)
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": os.getenv("FCM_SERVER_KEY")
}

# Настройки SMS Aero (для отправки SMS)
SMSAERO_API_KEY = os.getenv("SMSAERO_API_KEY")
SMSAERO_EMAIL = os.getenv("SMSAERO_EMAIL")
SMSAERO_FROM = os.getenv("SMSAERO_FROM")

# ==================================================
# Настройки REST Framework
# ==================================================

REST_FRAMEWORK = {
    # Аутентификация через JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Генерация схемы OpenAPI
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}

# Настройки для drf-spectacular (OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Doctor Management API',
    'DESCRIPTION': 'API for managing doctors, their specialties, workplaces, and schedules.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Настройки JWT (JSON Web Tokens)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ==================================================
# Настройки электронной почты
# ==================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# ==================================================
# Middleware
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CACHE_MIDDLEWARE_SECONDS = 0  # Отключаем кэширование

# ==================================================
# Настройки URL и шаблонов
# ==================================================

ROOT_URLCONF = 'rating.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rating.wsgi.application'

# ==================================================
# Настройки базы данных
# ==================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# ==================================================
# Валидация паролей
# ==================================================

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

# ==================================================
# Локализация и время
# ==================================================

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Dushanbe'
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('tg', 'Tajik'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
# ==================================================
# Статические файлы и медиа
# ==================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    '/var/www/rating/static/',
]

# Тип поля для первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==================================================
# Настройки django-storages (MinIO/S3)
# ==================================================

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')

AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = 'ru-central1'

MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"