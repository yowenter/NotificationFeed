import logging
from stream_framework.activity import Activity
from noti_feed.feed import IssueVerb, ManagerNotificationFeed
from models.issue import Issues

LOG = logging.getLogger(__name__)


def new_issues(user_id: str, issues: Issues):
    feed = ManagerNotificationFeed(user_id)
    issue_activities = [Activity(1, IssueVerb, issue, extra_context=issue.as_dict()) for issue in issues]
    # feed.insert_activities(issue_activities)
    # feed.add_many(issue_activities)
    for activity in issue_activities:
        try:
            feed.insert_activity(activity)
            feed.add(activity)
        except Exception as e:
            LOG.warning("Add activity %s failure %s", activity, e)
