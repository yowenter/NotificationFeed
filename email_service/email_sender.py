import smtplib
import ssl
import logging
from models.notification import Notification

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from common.config import NETEASE_163_EMAIL, NETEASE_163_PASSWD, MANAGER_EMAIL

LOG = logging.getLogger(__name__)

smtp_server = "smtp.163.com"
port = 465

user = NETEASE_163_EMAIL
password = NETEASE_163_PASSWD

# Create a secure SSL context
context = ssl.create_default_context()


def send_notification(notification: Notification):
    # https://www.spritecloud.com/2010/03/creating-and-sending-html-e-mails-with-python/
    message = MIMEMultipart('alternative')

    message['From'] = NETEASE_163_EMAIL
    # message['To'] = MANAGER_EMAIL
    message['Subject'] = notification.get_title()

    # message.preamble = notification.summary()

    message.attach(MIMEText(notification.render_html(), "HTML"))
    try:
        mail_server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        mail_server.login(user, password)
        mail_server.send_message(message, to_addrs=MANAGER_EMAIL.split(','))

    except Exception as e:
        LOG.warning("Send Email failure %s", str(e))
        return -1
    else:
        LOG.info("Send Email %s to %s success.", notification.get_title(), MANAGER_EMAIL)
        return 1


# if __name__ == '__main__':
#     from models.notification import IssuesNotification
#     from models.issue import NotificationIssue
#
#     send_notification(IssuesNotification("[GitHub Issue 更新] 2019-03-01 你有 8 条新消息未读 ",
#
#                                          [NotificationIssue("12345", "项目 飞天计划 更新", ["test", "kind/bug"],
#                                                             "https://github.com/repos/realityone/docker-image-py/issues/1")]
#                                          ))
