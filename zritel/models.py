import logging
import urllib.parse as urlparse

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

from website.models import StopWord
from zritel.collectors import VKCollector
from zritel.managers import SourceManager, RecordManager

logger = logging.getLogger(__name__)


class Source(models.Model):
    class Kind:
        VK = VKCollector.kind

        CHOICES = (
            (VK, 'ВКонтакте'),
        )

    title = models.CharField(max_length=512, help_text="Название источника")
    kind = models.CharField(max_length=36, choices=Kind.CHOICES)
    url = models.URLField(help_text="Ссылка")
    active = models.BooleanField(default=True)
    last_check_at = models.DateTimeField(blank=True, null=True, help_text="Время последней проверки")
    frequency = models.PositiveIntegerField(help_text="Частота Проверок")

    objects = SourceManager()

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return '{0.title} - {0.kind}'.format(self)

    @property
    def next_update_time(self):
        return self.last_check_at + timezone.timedelta(minutes=self.frequency)

    @property
    def group_name(self):
        return urlparse.urlparse(self.url).path.strip('/')

    @property
    def collector(self):
        if self.kind == VKCollector.kind:
            return VKCollector(source=self)
        raise NotImplementedError

    def scan_and_save_records(self):
        logger.info('Обзор {0.title} (id={0.pk})'.format(self))

        new_records = self.collector.harvest()

        Record.objects.bulk_create([
            Record(**record) for record in new_records
            if not Record.objects.filter(url=record['url']).exists()
        ])

        logger.info('Собрано {} новых записей'.format(len(new_records)))
        self.last_check_at = timezone.now()
        self.save()

    def schedule_scan(self):
        from zritel.tasks import collect_new_records
        collect_new_records.delay(source_id=self.pk)


class Record(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    url = models.URLField(help_text="Ссылка на текст")
    text = models.TextField(help_text="Текст")
    report = JSONField(blank=True, default=dict)
    processed = models.BooleanField(default=False)
    objects = RecordManager()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def process_text(self):
        clean_text = StopWord.pages.prepare_text(text=self.text)
        words = StopWord.objects.sanitize_text(clean_text)
        results = StopWord.objects.get_words_replacement(words)
        report = {w.keyword: w.replacement for w in results}
        self.report = report
        self.processed = True
        self.save()

    def schedule_processing(self):
        from zritel.tasks import label_record
        label_record.delay(record_id=self.pk)

    def __str__(self):
        return '{0.url} - {0.source}'.format(self)


@receiver(signals.post_save, sender=Source)
def trigger_scan(sender, instance, created, **kwargs):
    if created:
        instance.schedule_scan()


@receiver(signals.post_save, sender=Record)
def trigger_processing(sender, instance, created, **kwargs):
    if created:
        instance.schedule_processing()
