import time
from watcher.github_service import RepoIssueWatcher
from noti_feed.manager import new_issues


def main():
    k8s_repo = RepoIssueWatcher("kubernetes/kubernetes")
    prometheus_repo = RepoIssueWatcher("prometheus/prometheus")
    user_id = "manager"

    while 1:
        k8s_issues = k8s_repo.fetch_new_issues()
        prometheus_issues = prometheus_repo.fetch_new_issues()

        new_issues(user_id, k8s_issues + prometheus_issues)

        time.sleep(60)


if __name__ == '__main__':
    main()
