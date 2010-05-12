# Django settings for instamedia project.
import os, logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

logging.debug("Reading settings...")

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH + os.sep + 'static' + os.sep

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/static/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z@&gewj-htg(9k4(zx)mwtjo(4i9!zn)8l$z4d7ygr6q63^npn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', #for user template var
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media', #for MEDIA_URL template var
    'django.core.context_processors.request', #includes request in RequestContext
    'explainthis.questions.ctxproc.setting', #includes request in RequestContext
)

AUTHENTICATION_BACKENDS = (
    'django_rpx_plus.backends.RpxBackend', 
    'django.contrib.auth.backends.ModelBackend', #default django auth
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'explainthis.urls'

BASE_DOMAIN = "http://dev.explainthis.org:8000"

RPXNOW_API_KEY = "ab03bbe55691bf7ea5535a176848c99c39548c1e"
RPXNOW_APPLICATION_ID = "bgfakdbceknakngdnhgj"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + os.sep + 'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'ajaxcomments',
    'django.contrib.admin',
    'explainthis.questions',
    'django_rpx_plus',
    'compress',
    'voting',
    'uni_form',
    'taggit'
    
)

REGISTER_URL = '/accounts/register/'
RPXNOW_REALM = 'dev-explainthis'
AUTH_PROFILE_MODULE = "questions.UserProfile"
COMPRESS_CSS = {
    'main': {
        'source_filenames': (
            'css/lib/yui/reset-min.css',
            'css/lib/oocss/core/grid/grids.css',
            'css/lib/oocss/core/template/template.css',
            'css/main.css'
        ),
        'output_filename': 'css/main_compressed.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'forms': {
        'source_filenames': (
            'css/uni-form-generic.css',
            'css/uni-form.css'
        ),
        'output_filename': 'css/form_compressed.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    # other CSS groups goes here
}

COMPRESS_JS = {
    'base': {
        'source_filenames': (
            'js/lib/jquery-1.4.2.min.js',
            'js/main.js',          
        ),
        'output_filename': 'js/base_compressed.js',
    },
    'comments': {
        'source_filenames': (
            'js/post-comment.js',
            'js/comment.js',          
        ),
        'output_filename': 'js/comments_compressed.js',
    },
    'site_frontpage': {
        'source_filenames': (
            'js/lib/jquery-1.4.2.min.js',
            'js/lib/NobleCount/js/jquery.NobleCount.js',
            'js/site_frontpage.js'
        ),
        'output_filename': 'js/site_frontpage_compressed.js',
    }
}
COMPRESS = True
COMPRESS_AUTO = True

COMPRESS_CSS_FILTERS = None



LOCAL_SETTINGS = PROJECT_PATH + os.sep+ 'settings_local.py'

if os.path.exists(LOCAL_SETTINGS): execfile(LOCAL_SETTINGS)