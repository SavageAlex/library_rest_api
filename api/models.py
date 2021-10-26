import functools
from django.db import models

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=256)
    authors = models.TextField()
    published_date = models.DateField()
    categories = models.TextField()
    avaerage_rating = models.FloatField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title