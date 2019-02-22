from stream_framework.activity import Activity
from noti_feed.feed import IssueVerb, ManagerNotificationFeed


def new_issues(user_id, issues):
    feed = ManagerNotificationFeed(user_id)
    issue_activities = [Activity(None, IssueVerb, issue) for issue in issues]
    feed.add_many(issue_activities)

