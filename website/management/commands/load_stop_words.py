import csv

from django.core.management.base import BaseCommand

from website.models import StopWord


def load_file(filename):
    with open(filename, 'r') as finp:
        reader = csv.DictReader(finp)
        for word in reader:
            is_active = bool(word.get('использовать')) if word.get('использовать') else True
            StopWord.objects.update_or_create(
                keyword=word['слово'],
                defaults={
                    'keyword': word['слово'].lower(),
                    'replacement': word['замена'].lower(),
                    'active': is_active,
                })


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        filename = options['file_path']
        load_file(filename)
