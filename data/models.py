from django.db import models


class Keyword(models.Model):

    keyword = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class Result(models.Model):

    keyword = models.ForeignKey('Keyword')
    url = models.URLField()
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class Content(models.Model):

    result = models.ForeignKey('Result')
    html = models.TextField()
    title = models.TextField(null=True)
    body = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
