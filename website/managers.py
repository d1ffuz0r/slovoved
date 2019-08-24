import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.db import models


class StopWordManager(models.Manager):
    def sanitize_text(self, text):
        index = 0
        for w in re.split(r'\s', text):
            original = w.replace('%', ' ')
            length = len(w)
            sanitized = re.sub(r'[^А-яёЁA-z0-9\-\s]', '', w.strip('- ,:!')).replace('-', ' | ')
            yield (original, sanitized, index, length)
            index += (length + 1)

    def get_words_replacement(self, words):
        values = ", ".join("('{0}', '{1}', {2}, {3})".format(*word) for word in words)
        sql = '''WITH words_to_check(original, sanitized, position, length) AS (values {values})
SELECT st.id as id,
       st.keyword as keyword,
       st.replacement as replacement,
       words_to_check.original as original,
       words_to_check.sanitized as sanitized,
       words_to_check.position as position,
       words_to_check.length as length
FROM website_stopword AS st
JOIN words_to_check
    ON to_tsvector('russian', st.keyword) @@ to_tsquery('russian', words_to_check.sanitized);
'''.format(values=values)
        return self.get_queryset().raw(sql)


class WebsitePageManager(models.Manager):
    def prepare_text(self, html=None, text=None):
        if html:
            cleantext = BeautifulSoup(html, "lxml").text
        else:
            cleantext = text
        cleantext = re.sub(r'\t|\r\n|\n|\/', ' ', cleantext)
        cleantext = re.sub(r'<.*?>', ' ', cleantext)
        cleantext = re.sub(r'[^А-Яа-яёЁ\s]', ' ', cleantext)
        cleantext = re.sub(r'\s{1,}', ' ', cleantext)
        cleantext = cleantext.strip()
        return cleantext

    def process_page(self, content, results):
        processed = set([])
        for result in results:
            if result.replacement in processed or not result.replacement:
                continue
            processed.add(result.replacement)

            tmpl = ' <b style=\"background-color: #ffb62752; padding: 3px 2px; margin: 0 -2px; color: #e94b3d; font-style: normal; border-radius: .2em;\">{o} ({r})</b>'
            content = re.sub(
                '\s' + result.original,
                tmpl.format(o=result.original, r=result.replacement),
                content
            )

        return content

    def fix_links(self, content, url):
        ur = urlparse(url)
        base_url = '{}://{}/'.format(ur.scheme, ur.hostname)
        content = re.sub(r'="/', '="' + base_url, content)
        content = re.sub(r"='/", "='" + base_url, content)
        return content
