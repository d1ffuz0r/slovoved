from django.contrib import admin

from zritel.models import Source, Record


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'kind', 'active', 'last_check_at']
    list_filter = ['kind', 'active', 'alert_enabled']
    search_fields = ['title', 'url', 'slug']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['url', 'source']
    list_filter = ['source', 'processed']
    raw_id_fields = ['source']
