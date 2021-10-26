from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    published_date = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.title