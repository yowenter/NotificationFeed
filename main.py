import os
import time
import logging
import signal
import sys
from noti_feed import setup_feed
setup_feed()

from datetime import datetime
from watcher.github_service import RepoIssueWatcher
from noti_feed.manager import new_issues
from noti_feed.feed import ManagerNotificationFeed
from models.notification import IssuesNotification
from models.issue import NotificationIssue
from common.config import PROD
from email_service.email_sender import send_notification
import errno

logging.basicConfig(stream=sys.stdout, level=logging.INFO if PROD == 'true' else logging.DEBUG)

logging.getLogger("stream_framework").setLevel(logging.WARN)
logging.getLogger("urllib3").setLevel(logging.WARN)
logging.getLogger("github").setLevel(logging.WARN)

LOG = logging.getLogger(__name__)

MANAGER = "manager"



def notification_watcher():
    LOG.info("Starting repo issue watch service...")
    k8s_repo = RepoIssueWatcher("kubernetes/kubernetes")
    prometheus_repo = RepoIssueWatcher("prometheus/prometheus")
    test_repo = RepoIssueWatcher("yowenter/findtypo")

    while 1:
        issues = []
        k8s_issues = k8s_repo.fetch_new_issues()
        prometheus_issues = prometheus_repo.fetch_new_issues()
        test_issues = test_repo.fetch_new_issues()
        if test_issues:
            issues.extend(test_issues)
        if k8s_issues:
            issues.extend(k8s_issues)
        if prometheus_issues:
            issues.extend(prometheus_issues)
        notification_issues = [NotificationIssue.from_github_issue(i) for i in issues]
        LOG.info("New notification issues  %s queued.", len(notification_issues))
        new_issues(MANAGER, notification_issues)

        time.sleep(180)


def notification_consumer():
    LOG.info("Starting notification sender service...")
    feed = ManagerNotificationFeed(MANAGER)

    while True:
        activities = feed[:]
        issues = [NotificationIssue.from_dict(activity.extra_context) for activity in activities]
        title = "[GitHub Issue 提醒 ] {0} 你有 {1} 条新消息未读".format(datetime.now().date(), len(activities))

        summary = title
        if len(issues) >= 1:
            LOG.info("Sending Message %s", title)
            notification = IssuesNotification(title, issues, summary)
            send_notification(notification)
            feed.remove_many(activities)
            [feed.remove_activity(ac) for ac in activities]

        time.sleep(1800)


class Manager(object):

    def __init__(self):
        self.WORKERS = {}
        self.exit_now = False
        self.healthy = True

    def spawn_worker(self, func):
        LOG.info("Spawning worker %s", func)
        pid = os.fork()
        if pid != 0:
            self.WORKERS[pid] = func
            return pid

        func()

    def kill(self, signum, frame):
        LOG.info("Killing self.")
        self.exit_now = True
        for k, v in self.WORKERS.items():
            LOG.info("Killing process %s %s", k, v)
            try:
                os.kill(k, signal.SIGKILL)
            except Exception as e:
                LOG.warning("Kill worker  %s failure %s", k, e)

        sys.exit(0)

    def start(self):
        start = datetime.now()
        self.spawn_worker(notification_watcher)
        self.spawn_worker(notification_consumer)
        while 1:
            time.sleep(10)
            if self.exit_now:
                LOG.info("Gracefully stop.")
                break
            if not self.healthy:
                LOG.error("Manager unhealthy, exiting.")
                self.kill(signal.SIGKILL, None)
                sys.exit(1)

            LOG.info("Heartbeat, stay alive since `%s`.for %s", start, datetime.now() - start)
            LOG.debug("Workers %s", self.WORKERS)

            for pid, name in self.WORKERS.items():
                _, err_code = os.waitpid(pid, os.WNOHANG)
                LOG.debug("Wait pid %s err_code %s ", pid, err_code)
                if err_code != 0:
                    LOG.warning("Process %s %s unhealthy", pid, name)
                    self.healthy = False

                try:
                    os.kill(pid, 0)
                except OSError as e:
                    if e.errno == errno.ESRCH:
                        LOG.warning("Process %s %s not running", pid, name)
                    else:
                        LOG.warning("Process %s %s unknown state %s", pid, name, e)
                    LOG.info("Worker states not healthy. Exiting")
                    self.healthy = False

                else:
                    LOG.debug("Process %s %s is running", pid, name)


def main():
    manager = Manager()

    signal.signal(signal.SIGINT, manager.kill)
    signal.signal(signal.SIGTERM, manager.kill)

    manager.start()

    # notification_watcher()
    # notification_consumer()


# start 2 processes,
# one for watcher
# one for consumer


if __name__ == '__main__':
    main()
