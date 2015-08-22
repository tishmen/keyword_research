from django.contrib import admin, messages

from data.models import Keyword, Result, Content, Summary, Statistic
from data.tasks import (
    scrape_google_results_task, scrape_google_result_count_task,
    scrape_contents_task, create_summary_task, process_contents_task
)


class SummaryInline(admin.StackedInline):

    model = Summary
    extra = 0


class StatisticInline(admin.StackedInline):

    model = Statistic
    extra = 0


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    list_display = ('keyword', 'result_count')
    actions = ('scrape_google_results', 'scrape_google_result_count')

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

    def scrape_google_result_count(self, request, queryset):
        count = queryset.count()
        for keyword in queryset:
            scrape_google_result_count_task.delay(keyword)
        if count == 1:
            message_bit = '1 keyword'
        else:
            message_bit = '{} keywords'.format(count)
        self.message_user(
            request,
            'Delayed scrape_google_result_count_task for {}'.format(
                message_bit
            ),
            level=messages.SUCCESS
        )

    scrape_google_results.short_description = 'scrape_google_results for sele'\
        'cted keywords'
    scrape_google_result_count.short_description = 'scrape_google_result_coun'\
        't for selected keywords'


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

    list_display = ('result', 'title', 'word_count')
    exclude = ('html', 'body_html')
    actions = ('process_contents', 'create_summary')
    inlines = (SummaryInline, StatisticInline)

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

    def create_summary(self, request, queryset):
        count = queryset.count()
        for content in queryset:
            create_summary_task.delay(content)
        if count == 1:
            message_bit = '1 content'
        else:
            message_bit = '{} contents'.format(count)
        self.message_user(
            request,
            'Delayed create_summary_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    process_contents.short_description = 'process_contents for selected conte'\
        'nts'
    create_summary.short_description = 'create_summary for selected contents'
