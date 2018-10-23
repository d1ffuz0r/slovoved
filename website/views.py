import json

from django.views.generic import View, TemplateView
from django.core.exceptions import ValidationError
from django.views.generic.base import HttpResponse

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
        text = str(json.loads(request.body).get('text', ''))
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
