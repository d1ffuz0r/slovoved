from django.contrib import admin

from website.models import StopWord


@admin.register(StopWord)
class StopWordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'replacement', 'active')
    search_fields = ('keyword', 'replacement')
    list_filter = ('active',)
