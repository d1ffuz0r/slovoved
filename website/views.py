import json
import re

from django.views.generic import View, TemplateView
from django.core.exceptions import ValidationError
from django.views.generic.base import HttpResponse

from website.models import StopWord


class IndexView(TemplateView):
    template_name = 'index.html'


class SlovovedView(TemplateView):
    template_name = 'slovoved.html'


class ValidationView(View):
    def post(self, request):
        text = request.POST.get('text')
        if not text:
            raise ValidationError('Нет данных в text')

        candidates = (
            (word, re.sub(r'[^A-zА-я0-9\- ]', '', word))
            for word in text.split()
        )

        results = StopWord.objects.get_words_replacement(candidates)
        results = [
            {
                'original': r.original,
                'keyword': r.keyword,
                'replacement': r.replacement
            } for r in results
        ]
        return HttpResponse(json.dumps(results), content_type='application/json')
