from django.db import models
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
