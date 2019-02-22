from github import Github
from common.config import GITHUB_ACCESS_TOKEN

github_client = Github(GITHUB_ACCESS_TOKEN)


class RepoIssueWatcher(object):
    def __init__(self, repo_full_name):
        self.current_issue_no = 1
        self.repo_full_name = repo_full_name
        self.repo = None

    def fetch_new_issues(self):
        if not self.repo:
            self.repo = github_client.get_repo(self.repo_full_name)

        issues = self.repo.get_issues(state='open').get_page(0)

        if self.current_issue_no >= issues[0].number:
            # no new issue found
            return

        new_issues = [issue for issue in issues if issue.number > self.current_issue_no]
        self.current_issue_no = issues[0].number
        return new_issues

# if __name__ == '__main__':
#     repo_watcher = RepoIssueWatcher('kubernetes/kubernetes')
#     print(repo_watcher.fetch_new_issues())
