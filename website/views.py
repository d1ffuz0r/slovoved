import json

import requests
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.views.generic import View, TemplateView, ListView
from django.views.generic.base import HttpResponse

from website.models import StopWord
from zritel.models import Source, Record


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

        clean_text = StopWord.pages.prepare_text(html=content)
        words = StopWord.objects.sanitize_text(clean_text)
        results = StopWord.objects.get_words_replacement(words)
        content = StopWord.pages.process_page(content, results)
        content = StopWord.pages.fix_links(content, url)

        return HttpResponse(content)


class SaitovedView(ListView):
    template_name = 'saitoved_sources.html'
    queryset = Source.objects.all().annotate(cnt=Count('record')).order_by('-last_check_at')


class RecordsView(ListView):
    template_name = 'saitoved_records.html'
    queryset = Record.objects.all().order_by('added_at')
    paginate_by = 10

    def get_queryset(self):
        queryset = super(RecordsView, self).get_queryset()
        queryset = queryset.filter(source_id=self.kwargs['pk'])
        return queryset
