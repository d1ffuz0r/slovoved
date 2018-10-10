from django.db import models


class StopWordManager(models.Manager):
    def get_words_replacement(self, words, score=0.6):
        sql = """"""
        for index, w in enumerate(words):
            if index > 0:
                sql += 'UNION\n'
            sql += """SELECT id, keyword, replacement, '{0}' as original, similarity(keyword, '{1}') as sml
          FROM website_stopword
          WHERE keyword %% '{1}'\n""".format(*w)

        results = self.get_queryset().raw(sql)
        results = [r for r in results if r.sml >= score]

        return results

