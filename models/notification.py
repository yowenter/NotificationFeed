import os

from typing import List
from jinja2 import Template
from models.issue import Issues

notification_tmpl_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
                                      "notification.tmpl")

with open(notification_tmpl_path, 'r') as f:
    NOTIFICATION_TEMPLATE = Template(f.read())


class Notification(object):

    def get_title(self):
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def render_html(self):
        raise NotImplementedError

    @property
    def messages(self):
        raise NotImplementedError


class SimpleMessage(object):
    def __init__(self, url, summary, tags=None):
        self.url = url
        self.summary = summary
        self.tags = ','.join(tags) if tags else ''


SimpleMessages = List[SimpleMessage]


class IssuesNotification(Notification):

    def __init__(self, title: str, issues: Issues, summary=''):
        self.issues = issues
        self.title = title
        self.summary_txt = summary

    def get_title(self):
        return self.title

    def summary(self):
        return self.summary_txt

    def render_html(self):
        return NOTIFICATION_TEMPLATE.render(summary=self.summary(), title=self.title, messages=self.messages)

    @property
    def messages(self) -> SimpleMessages:
        return [SimpleMessage(issue.url, "#{0} [{1}]: {2}".format(issue.id, issue.repo_name, issue.title), issue.labels)
                for issue in
                self.issues[:20]]

# if __name__ == '__main__':
#     from models.issue import NotificationIssue
#
#     issues = [NotificationIssue(i, "Example", [], "https://api.github.com/repos/kubernetes/kubernetes/issues/74446") for
#               i in range(10)]
#     print(IssuesNotification("Example", issues, 'summary').render_html())
