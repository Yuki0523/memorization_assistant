from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'assistant': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',
            'interval': 1,
            'backupCount': 7
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prods': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s',
                '%(pathname)s(Line:%(lineno)d',
                '%(message)s',
            ])
        },
    },
}
