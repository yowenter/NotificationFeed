import os

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

NETEASE_163_EMAIL = os.getenv("NETEASE_163_EMAIL")
NETEASE_163_PASSWD = os.getenv("NETEASE_163_PASSWD")

MANAGER_EMAIL = os.getenv("MANAGER_EMAIL")


PROD = os.getenv("PROD", "false")
