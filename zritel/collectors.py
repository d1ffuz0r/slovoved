import requests
from django.conf import settings


class VKCollector(object):
    """
    Документация по сбору записей https://vk.com/dev/wall.get
    """
    kind = 'vk'

    def __init__(self, source):
        self.source = source

    def harvest(self):
        records = self.pull_new_records()
        return [self.transform_record(record) for record in records]

    def pull_new_records(self):
        url = 'https://api.vk.com/method/wall.get'
        args = {
            'access_token': settings.VK_API_KEY,
            'domain': self.source.group_name,
            'v': 5.84,
            'count': 20,
        }
        response = requests.get(url=url, params=args).json()
        return response['response']['items']

    def transform_record(self, record):
        return {
            'source': self.source,
            'text': record['text'],
            'url': '{}?w=wall{}_{}'.format(self.source.url, int(record['owner_id']), record['id'])
        }
