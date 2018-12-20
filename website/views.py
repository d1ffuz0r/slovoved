import json

from django.views.generic import View, TemplateView
from django.core.exceptions import ValidationError
from django.views.generic.base import HttpResponse
import requests

from website.models import StopWord


class IndexView(TemplateView):
    template_name = 'index.html'


class SlovovedView(TemplateView):
    template_name = 'slovoved.html'


class WordValidationView(View):
    def serialize(self, record):
        return {
            'original': record.original,
            'replacement': record.replacement,
            'position': record.position,
            'length': record.length
        }

    def post(self, request):
        text = json.loads(request.body.decode()).get('text', '')
        if not text:
            raise ValidationError('Нет данных в words')

        words = list(StopWord.objects.sanitize_text(text))
        results = StopWord.objects.get_words_replacement(words)
        results = [self.serialize(record) for record in results]

        output = {
            'results': results,
            'bad_count': len(results),
            'total_count': len(words)
        }
        return HttpResponse(json.dumps(output), content_type='application/json')


class WebovedView(TemplateView):
    template_name = 'weboved.html'


class LoadUrlView(View):
    def get(self, request):
        url = request.GET.get('url')
        response = requests.get(url, timeout=5)
        content = response.content.decode('utf-8')

        clean_text = StopWord.pages.prepare_text(content)
        words = StopWord.objects.sanitize_text(clean_text)
        results = StopWord.objects.get_words_replacement(words)
        content = StopWord.pages.process_page(content, results)
        content = StopWord.pages.fix_links(content, url)

        return HttpResponse(content)
