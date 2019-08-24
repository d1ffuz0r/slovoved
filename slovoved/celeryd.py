"""
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slovoved.settings')

app = Celery('slovoved')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
