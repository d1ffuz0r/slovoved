from slovoved.settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()]
)
