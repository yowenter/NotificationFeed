import smtplib
import ssl
from models.notification import Notification

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from common.config import NETEASE_163_EMAIL, NETEASE_163_PASSWD, MANAGER_EMAIL

smtp_server = "smtp.163.com"
port = 465

user = NETEASE_163_EMAIL
password = NETEASE_163_PASSWD

# Create a secure SSL context
context = ssl.create_default_context()

mail_server = smtplib.SMTP_SSL(smtp_server, port, context=context)
mail_server.login(user, password)


def send_notification(notification: Notification):
    # https://www.spritecloud.com/2010/03/creating-and-sending-html-e-mails-with-python/
    message = MIMEMultipart('alternative')

    message['From'] = NETEASE_163_EMAIL
    message['To'] = MANAGER_EMAIL
    message['Subject'] = notification.get_title()

    message.preamble = notification.summary()

    message.attach(MIMEText(notification.render_html(), "HTML"))

    mail_server.send_message(message)
