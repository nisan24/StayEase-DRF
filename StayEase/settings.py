from pathlib import Path
import os
import environ
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

env = environ.Env()
environ.Env.read_env()


# print(env("DB_NAME")) 
# print(env("USER")) 
# print(env("PASSWORD")) 
# print(env("HOST")) 
# print(env("PORT")) 
# print(env("DB_NAME")) 


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env('SECRET_KEY')

DEBUG = True

# ALLOWED_HOSTS = ['.vercel.app']
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://stayease-drf.onrender.com', 'https://*.127.0.0.1',]
CORS_ALLOW_ALL_ORIGINS = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'corsheaders',
    'cloudinary',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "accounts",
    "bookings",
    "hotels",
    "reviews",
    "payments",  
]


LOGIN_URL = '/accounts/login/'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StayEase.urls'

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

WSGI_APPLICATION = 'StayEase.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('dbname'),
        'USER': env("user"),
        'PASSWORD': env("password"),
        'HOST': env("host"),
        'PORT': env("port")
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# --------- Send mail setup ---------
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# Default vabe Name show korar jonno
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# --------- SSLCOMMERZ ER ---------
STORE_ID = env("STORE_ID")
STORE_PASS = env("STORE_PASS")
IS_SANDBOX = env("IS_SANDBOX")



CLOUDINARY_URL='cloudinary://861881146933254:ocATWcFnFyD--CbmsPpAXfsOJOE@dfqwj2lfu'

cloudinary.config( 
  cloud_name = 'dfqwj2lfu',  
  api_key = '861881146933254',  
  api_secret = 'ocATWcFnFyD--CbmsPpAXfsOJOE',
  secure= True
)