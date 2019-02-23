import logging
import re
from github import Issue
from typing import List

LOG = logging.getLogger(__name__)


class NotificationIssue(object):
    def __init__(self, issue_id, title, labels, url):
        self.id = issue_id
        self.title = title
        self.labels = labels
        self.url = url
        try:
            self.repo_name = re.search("github.com/(.*)/issue", url).groups()[0]
        except Exception as e:
            LOG.warning("Unknown issue  %s repo name, error %s ", url, e)
            self.repo_name = ""

    @classmethod
    def from_github_issue(cls, issue: Issue):
        return cls(
            issue.number,
            issue.title,
            [label.name for label in issue.labels],
            issue.url.replace("api.github.com/repos", "github.com")
        )

    def as_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            labels=self.labels,
            url=self.url,
            repo_name=self.repo_name
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['title'],
            data.get('labels'),
            data['url']
        )


Issues = List[NotificationIssue]
