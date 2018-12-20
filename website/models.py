from django.db import models

from website.managers import StopWordManager, WebsitePageManager


class StopWord(models.Model):
    keyword = models.CharField(
        max_length=512,
        verbose_name='Слово',
        unique=True)
    replacement = models.CharField(
        max_length=512,
        verbose_name='Русская Замена')
    active = models.BooleanField(default=True)

    objects = StopWordManager()
    pages = WebsitePageManager()

    def __str__(self):
        return '{0.keyword} - {0.replacement}'.format(self)
