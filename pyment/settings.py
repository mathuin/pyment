# Django settings for pyment project.

from decouple import config, Csv
from unipath import Path
from dj_database_url import parse as db_url

SITE_ROOT = Path(__file__).parent.parent

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
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

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
    SITE_ROOT.child('templates', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'utils.context_processors.pyment',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pyment.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pyment.wsgi.application'

TEMPLATE_DIRS = (
    SITE_ROOT.child('templates'),
)

LOGIN_REDIRECT_URL = '/accounts/my_account'
AUTH_PROFILE_MODULE = 'accounts.userprofile'
PRODUCTS_PER_PAGE = 12
PRODUCTS_PER_ROW = 4
SESSION_AGE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_AGE_DAYS
INACTIVE_JAR_AGE_DAYS = 14

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
    'utils',
    'cart',
    'checkout',
    'accounts',
    'search',
    'stats',
    'meadery',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
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
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# New test runner as of 1.6
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
