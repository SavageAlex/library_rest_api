from django.db import models

class Author(models.Model):
    author_name = models.CharField(primary_key=True, unique=True, max_length=255)

    class Meta:
        ordering = ['author_name']

    def __str__(self):
        return self.author_name

class Category(models.Model):
    category_name = models.CharField(primary_key=True, unique=True, max_length=255)

    class Meta:
        ordering = ['category_name']


    def __str__(self):
        return self.category_name

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, blank=True)
    published_date = models.DateField(null=True, blank=True) # must accepting a full date and yeat only formats
    categories = models.ManyToManyField(Category, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
