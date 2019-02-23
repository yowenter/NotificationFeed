from stream_framework.feeds.aggregated_feed.notification_feed import RedisNotificationFeed
from stream_framework.verbs.base import Verb
from stream_framework.aggregators.base import BaseAggregator


# https://stream-framework.readthedocs.io/en/latest/notification_systems.html

class ManagerNotificationFeed(RedisNotificationFeed):
    # : they key format determines where the data gets stored
    key_format = 'feed:notification:%(user_id)s'


class IssueVerb(Verb):
    id = 5
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
