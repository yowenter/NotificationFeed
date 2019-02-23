import logging
from urllib.parse import urlparse
from common.config import REDIS_URL
from stream_framework import default_settings

LOG = logging.getLogger(__name__)


def setup_feed():
    redis_config = urlparse(REDIS_URL)

    LOG.info("Initialize redis config for stream feed %s", REDIS_URL)

    default_settings.STREAM_REDIS_CONFIG = {
        'default': {
            'host': redis_config.hostname,
            'port': redis_config.port,
            'db': redis_config.path[1:],
            'password': None
        },
    }

    from noti_feed.feed import IssueVerb
    from stream_framework.verbs import register
    register(IssueVerb)
