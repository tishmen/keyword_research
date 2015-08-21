from django.db import models


class Keyword(models.Model):

    keyword = models.TextField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class Result(models.Model):

    keyword = models.ForeignKey('Keyword')
    url = models.TextField()
    position = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class Link(models.Model):

    url = models.TextField()

    def __str__(self):
        return self.url


class Content(models.Model):

    result = models.ForeignKey('Result')
    links = models.ManyToManyField('Link')
    html = models.TextField()
    title = models.TextField()
    body_html = models.TextField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
