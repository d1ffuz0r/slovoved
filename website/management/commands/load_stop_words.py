import csv

from django.core.management.base import BaseCommand

from website.models import StopWord


def load_file(filename):
    with open(filename, 'r') as finp:
        reader = csv.DictReader(finp)
        for word in reader:
           StopWord.objects.update_or_create(
               keyword=word['keyword'],
               defaults={
                   'keyword': word['keyword'].lower(),
                   'replacement': word['replacement'].lower(),
                   'active': bool(word.get('active')) if word.get('active') else True,
               })


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        filename = options['file_path']
        load_file(filename)
