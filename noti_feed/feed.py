# from stream_framework.feeds.aggregated_feed.notification_feed import RedisNotificationFeed
from stream_framework.verbs.base import Verb
from stream_framework.aggregators.base import BaseAggregator

from stream_framework.feeds.redis import RedisFeed

from stream_framework.storage.redis.activity_storage import RedisActivityStorage
from stream_framework.storage.redis.timeline_storage import RedisTimelineStorage


# https://stream-framework.readthedocs.io/en/latest/notification_systems.html

class ManagerNotificationFeed(RedisFeed):
    pass


class IssueVerb(Verb):
    id = 10
    infinitive = 'issue'
    past_tense = 'issued'


class VerbDailyAggregator(BaseAggregator):
    '''
    Aggregates based on the same verb and same time period
    '''

    def get_group(self, activity):
        '''
        Returns a group based on the day and verb
        '''
        verb = activity.verb.id
        date = activity.time.date()
        group = '%s-%s' % (verb, date)
        return group
