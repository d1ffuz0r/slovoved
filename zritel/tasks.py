import logging

from celery.schedules import crontab
from celery.task import periodic_task, task

from zritel.models import Source, Record

logger = logging.getLogger(__name__)

SCHEDULE_OFFSET = 60


@periodic_task(run_every=crontab(hour='*', minute=0))
def check_for_new_records(force=False):
    queryset = Source.objects.available_for_updates(offset=SCHEDULE_OFFSET, force=force)
    logger.info('Обзор {} источников'.format(queryset.count()))
    for source in queryset:
        source.schedule_scan()


@periodic_task(run_every=crontab(hour='*', minute=0))
def label_new_records():
    queryset = Record.objects.available_for_labeling()
    logger.info('Обработка {} новых записей'.format(queryset.count()))
    for record in queryset:
        record.schedule_labeling()


@task()
def collect_new_records(source_id):
    source = Source.objects.get(pk=source_id)
    source.scan_and_save_records()


@task()
def label_record(record_id):
    record = Record.objects.select_related('source').get(pk=record_id)
    record.process_text()
