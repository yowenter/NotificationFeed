


class MyAggregator(BaseAggregator):
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


# feed = MyNotificationFeed(user_id)
# activity = Activity(
#     user_id, LoveVerb, object_id, influencer_id, time=created_at,
#     extra_context=dict(entity_id=self.entity_id)
# )
# feed.add(activity)
# print feed[:5]


class MyNotification(object):
    '''
    Abstract the access to the notification feed
    '''
    def add_love(self, love):
        feed = MyNotificationFeed(user_id)
        activity = Activity(
            love.user_id, LoveVerb, love.id, love.influencer_id,
            time=love.created_at, extra_context=dict(entity_id=self.entity_id)
        )
        feed.add(activity)
