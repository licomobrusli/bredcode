# logging_config.py

import os
from django.utils.log import DEFAULT_LOGGING

# Directory where logs should be stored
LOGGING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# Ensure the directory exists
os.makedirs(LOGGING_DIR, exist_ok=True)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        #######
        # a general logger when using logging.debug without specifying the logger
        "": {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',  # lowest level (active for DEBUG, ERROR, CRITICAL, FATAL)
            'propagate': True,
        },
        #######
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}