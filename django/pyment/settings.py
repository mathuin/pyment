# Django settings for pyment project.

from decouple import config, Csv
from unipath import Path
from dj_database_url import parse as db_url
from dj_email_url import parse as email_url

BASE_DIR = Path(__file__).parent.parent

PUBLIC_ROOT = Path(config('PUBLIC_ROOT'))

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

TRAVIS = config('TRAVIS', default=False, cast=bool)

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url
    )
}

SITE_NAME = config('SITE_NAME', default='Site Name')
META_KEYWORDS = config('META_KEYWORDS', default='meta')
META_DESCRIPTION = config('META_DESCRIPTION', default='meta description')
BREWER_NAME = config('BREWER_NAME', default='Joe Brewer')
BREWER_EMAIL = config('BREWER_EMAIL', default='brewer@example.com')
BREWER_LOCATION = config('BREWER_LOCATION', default='Anywhere, USA')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    (BREWER_NAME, BREWER_EMAIL),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', default=False)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows configironment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PUBLIC_ROOT.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PUBLIC_ROOT.child('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY')

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.pyment',
            ]
        }
    }
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pyment.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pyment.wsgi.application'

LOGIN_REDIRECT_URL = '/accounts/my_account'
AUTH_PROFILE_MODULE = 'accounts.userprofile'
PRODUCTS_PER_PAGE = 12
PRODUCTS_PER_ROW = 4
SESSION_AGE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_AGE_DAYS
INACTIVE_JAR_AGE_DAYS = 14

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    # 'django.contrib.flatpages',
    'inventory',
    'utils',
    'cart',
    'checkout',
    'accounts',
    'search',
    'stats',
    'meadery',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Email!
EMAIL_URL = config('EMAIL_URL', default='')
email_config = email_url(EMAIL_URL)
EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
# EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# New test runner as of 1.6
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
