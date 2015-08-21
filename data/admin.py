from django.contrib import admin

from data.models import Keyword, Result


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = ('keyword', 'url', 'position')
