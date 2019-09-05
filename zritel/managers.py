from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class SourceManager(models.Manager):
    def available_for_updates(self, offset, force=False):
        queryset = self.get_queryset()
        if not force:
            queryset = queryset.filter(
                last_check_at__lte=timezone.now() - timezone.timedelta(minutes=offset)
            )
        return queryset


class RecordManager(models.Manager):
    def available_for_labeling(self):
        queryset = self.get_queryset()
        queryset = queryset.filter(processed=False)
        return queryset

    def bulk_create(self, objs, **kwargs):
        results = super().bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)
        return results
