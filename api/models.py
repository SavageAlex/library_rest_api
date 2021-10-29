from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['author_name']

    def __str__(self):
        return self.author_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['category_name']


    def __str__(self):
        return self.category_name

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    published_date = models.DateField()
    categories = models.ManyToManyField(Category)
    avaerage_rating = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    thumbnail = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
