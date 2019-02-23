from stream_framework.activity import Activity
from noti_feed.feed import IssueVerb, ManagerNotificationFeed
from models.issue import Issues


def new_issues(user_id: str, issues: Issues):
    feed = ManagerNotificationFeed(user_id)
    issue_activities = [Activity(None, IssueVerb, issue) for issue in issues]
    feed.add_many(issue_activities)


