from django.db import models


class Keyword(models.Model):

    keyword = models.CharField(max_length=100, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class Result(models.Model):

    keyword = models.ForeignKey('Keyword')
    url = models.URLField()
    position = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
