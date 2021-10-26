from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'published_date', 'categories', 'avaerage_rating', 'ratings_count', 'thumbnail')
