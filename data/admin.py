from django.contrib import admin, messages

from data.models import Keyword, Result
from data.tasks import scrape_google_results_task


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
