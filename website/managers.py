import re

from django.db import models


class StopWordManager(models.Manager):
    def sanitize_text(self, text):
        index = 0
        for w in re.split(r'\s', text):
            original = w
            length = len(w)
            sanitized = re.sub(r'[^А-яA-z0-9\- ]', '', w.strip('- ,:!')).replace('-', ' | ')
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
