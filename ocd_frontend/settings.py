import os.path

DEBUG = True

# Celery settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

# Elasticsearch
ELASTICSEARCH_HOST = '127.0.0.1'
ELASTICSEARCH_PORT = 9200

# The default number of hits to return for a search request via the REST API
DEFAULT_SEARCH_SIZE = 150

# The max. number of hits to return for a search request via the REST API
MAX_SEARCH_SIZE = 200000

# The name of the index containing documents from all sources
COMBINED_INDEX = 'tkv_combined_index'

# The default prefix used for all data
DEFAULT_INDEX_PREFIX = 'tkv'

# The fields which can be used for sorting results via the REST API
SORTABLE_FIELDS = {
    'items': [
        'meta.source_id', 'meta.processing_started', 'meta.processing_finished',
        '_score', 'date', 'period', 'id']
}

# EXCLUDED_FIELDS_DEFAULT = ['all_text', 'source_data',
#                            'media_urls.original_url',
#                            'combined_index_data']
# EXCLUDED_FIELDS_SEARCH = ['all_text', 'media_urls.original_url']
#
# ALLOWED_INCLUDE_FIELDS_DEFAULT = ['all_text', 'source_data']
# ALLOWED_INCLUDE_FIELDS_SEARCH = ['all_text']

EXCLUDED_FIELDS_ALWAYS = [
    'combined_index_data', 'enrichments', 'hidden']
EXCLUDED_FIELDS_DEFAULT = ['all_text', 'source_data',
                           'media_urls.original_url', 'data', 'fields']
EXCLUDED_FIELDS_SEARCH = ['all_text', 'media_urls.original_url', 'data', 'fields']

ALLOWED_INCLUDE_FIELDS_DEFAULT = ['data', 'fields']
ALLOWED_INCLUDE_FIELDS_SEARCH = ['data', 'fields']

SIMPLE_QUERY_FIELDS = {
    'items': [
        'name', 'description'],
    'persons': [
        'name', 'id']
}

DOC_TYPE_DEFAULT = u'items'

# Definition of the ES facets (and filters) that are accessible through
# the REST API
COMMON_FACETS = {
    'processing_started': {
        'date_histogram': {
            'field': 'meta.processing_started',
            'interval': 'month'
        }
    },
    'processing_finished': {
        'date_histogram': {
            'field': 'meta.processing_finished',
            'interval': 'month'
        }
    },
    'source': {
        'terms': {
            'field': 'meta.source_id',
            'size': 10
        }
    },
    'collection': {
        'terms': {
            'field': 'meta.collection',
            'size': 10
        }
    },
    'rights': {
        'terms': {
            'field': 'meta.rights',
            'size': 10
        }
    },
    'index': {
        'terms': {
            'field': '_index',
            'size': 10
        }
    },
    'types': {
        'terms': {
            'field': '_type',
            'size': 10
        }
    },
    'fields': {
        'nested': 'fields',
        'terms': {
            'field': 'fields.key',
            'size': 10
        }
    },
    'id': {
        'terms': {
            'field': 'id',
            'size': 10
        }
    }
}

AVAILABLE_FACETS = {
    'items': {
        'rights': {
            'terms': {
                'field': 'meta.rights',
                'size': 10
            }
        },
        'period': {
            'terms': {
                'field': 'period',
                'size': 10
            }
        },
        'date': {
            'date_histogram': {
                'field': 'date',
                'interval': 'month'
            }
        },
        'classification': {
            'terms': {
                'field': 'classification'
            }
        },
        'extension_classification': {
            'terms': {
                'field': 'extension.classification'
            }
        },
        'additional_answer_classification': {
            'terms': {
                'field': 'additional_answer.classification'
            }
        },
        'answer_classification': {
            'terms': {
                'field': 'answer.classification'
            }
        },
        'id': {
            'terms': {
                'field': 'id',
                'size': 10
            }
        },
        'questions_hash': {
            'terms': {
                'field': 'questions_hash',
                'size': 10
            }
        },
        'description': {
            'terms': {
                'field': 'description',
                'size': 10
            }
        },
        'answer_description': {
            'terms': {
                'field': 'answer.description',
                'size': 10
            }
        },
    }
}


# AVAILABLE_FACETS = {
#     # 'retrieved_at': {
#     #     'date_histogram': {
#     #         'field': 'retrieved_at',
#     #         'interval': 'month'
#     #     }
#     # },
#     'rights': {
#         'terms': {
#             'field': 'meta.rights',
#             'size': 10
#         }
#     },
#     'source_id': {
#         'terms': {
#             'field': 'meta.source_id',
#             'size': 10
#         }
#     },
#     'collection': {
#         'terms': {
#             'field': 'meta.collection'
#         }
#     },
#     'author': {
#         'terms': {
#             'field': 'authors.untouched',
#             'size': 10
#         }
#     },
#     'date': {
#         'date_histogram': {
#             'field': 'date',
#             'interval': 'month'
#         }
#     },
#     'date_granularity': {
#         'terms': {
#             'field': 'date_granularity',
#             'size': 10
#         }
#     },
#     'media_content_type': {
#         'terms': {
#             'field': 'media_urls.content_type',
#             'size': 10
#         }
#     }
# }


# For highlighting
COMMON_HIGHLIGHTS = {
    'source': {},
    'collection': {},
    'rights': {}
}

AVAILABLE_HIGHLIGHTS = {
    'items': {
        'name': {},
        'description': {}
    },
    'tk_questions': {
        'name': {},
        'description': {}
    }
}

# The allowed date intervals for an ES data_histogram that can be
# requested via the REST API
ALLOWED_DATE_INTERVALS = ('day', 'week', 'month', 'quarter', 'year')

# Name of the Elasticsearch index used to store URL resolve documnts
RESOLVER_URL_INDEX = 'tkv_resolver'

# Determines if API usage events should be logged
USAGE_LOGGING_ENABLED = True
# Name of the Elasticsearch index used to store logged events
USAGE_LOGGING_INDEX = 'tkv_usage_logs'

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DUMPS_DIR = os.path.join(os.path.dirname(ROOT_PATH), 'dumps')
LOCAL_DUMPS_DIR = os.path.join(os.path.dirname(ROOT_PATH), 'local_dumps')

# URL where of the API instance that should be used for management commands
# Should include API version and a trailing slash.
# Can be overridden in the CLI when required, for instance when the user wants
# to download dumps from another API instance than the one hosted by OpenState
API_URL = 'http://api.kamervragentracker.nl:5000/v0/'

LOGGING = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        'ocd_frontend': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

THUMBNAILS_TEMP_DIR = '/tmp'

THUMBNAILS_MEDIA_TYPES = {'image/jpeg', 'image/png', 'image/tiff'}
THUMBNAILS_DIR = os.path.join(ROOT_PATH, '.thumbnail-cache')

THUMBNAIL_SMALL = 250
THUMBNAIL_MEDIUM = 500
THUMBNAIL_LARGE = 1000

THUMBNAIL_SIZES = {
    'large': {'size': (THUMBNAIL_LARGE, THUMBNAIL_LARGE), 'type': 'aspect'},
    'medium': {'size': (THUMBNAIL_MEDIUM, THUMBNAIL_MEDIUM), 'type': 'aspect'},
    'small': {'size': (THUMBNAIL_SMALL, THUMBNAIL_SMALL), 'type': 'aspect'},
    'large_sq': {'size': (THUMBNAIL_LARGE, THUMBNAIL_LARGE), 'type': 'crop'},
    'medium_sq': {'size': (THUMBNAIL_MEDIUM, THUMBNAIL_MEDIUM), 'type': 'crop'},
    'small_sq': {'size': (THUMBNAIL_SMALL, THUMBNAIL_SMALL), 'type': 'crop'},
}

THUMBNAIL_URL = '/media/'


# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass
