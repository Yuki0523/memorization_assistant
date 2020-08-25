from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'assistant': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s',
                '%(pathname)s(Line:%(lineno)d',
                '%(message)s',
            ])
        },
    },
}
