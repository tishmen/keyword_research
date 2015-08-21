from django.contrib import admin, messages

from data.models import Keyword, Result, Content
from data.tasks import (
    scrape_google_results_task, scrape_contents_task, process_contents_task
)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    actions = ('scrape_google_results', )

    def scrape_google_results(self, request, queryset):
        count = queryset.count()
        for keyword in queryset:
            scrape_google_results_task.delay(keyword)
        if count == 1:
            message_bit = '1 keyword'
        else:
            message_bit = '{} keywords'.format(count)
        self.message_user(
            request,
            'Delayed scrape_google_results_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    scrape_google_results.short_description = 'scrape_google_results for sele'\
        'cted keywords'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = ('keyword', 'url', 'position')
    actions = ('scrape_contents', )

    def scrape_contents(self, request, queryset):
        count = queryset.count()
        for result in queryset:
            scrape_contents_task.delay(result)
        if count == 1:
            message_bit = '1 result'
        else:
            message_bit = '{} results'.format(count)
        self.message_user(
            request,
            'Delayed scrape_contents_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    scrape_contents.short_description = 'scrape_contents for selected results'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):

    list_display = ('result', 'title')
    exclude = ('html', 'body_html')
    actions = ('process_contents', )

    def process_contents(self, request, queryset):
        count = queryset.count()
        for content in queryset:
            process_contents_task.delay(content)
        if count == 1:
            message_bit = '1 content'
        else:
            message_bit = '{} contents'.format(count)
        self.message_user(
            request,
            'Delayed scrape_contents_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    process_contents.short_description = 'process_contents for selected conte'\
        'nts'
