from urllib.parse import urlparse
from common.config import REDIS_URL
from stream_framework import default_settings

redis_config = urlparse(REDIS_URL)
default_settings.STREAM_REDIS_CONFIG = {
    'default': {
        'host': redis_config.hostname,
        'port': redis_config.port,
        'db': redis_config.path[1:],
        'password': None
    },
}
