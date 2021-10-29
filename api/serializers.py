from rest_framework import serializers
from .models import Book, Author, Category

class AuthorSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
         return value.author_name

    class Meta:
        model = Author
        fields = ['author_name',]
        pass

class CategorySerializer(serializers.ModelSerializer):

    def to_representation(self, value):
         return value.category_name

    class Meta:
        model = Category
        fields = ['category_name',]
        pass

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'published_date', 'categories', 'avaerage_rating', 'ratings_count', 'thumbnail']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        categories_data = validated_data.pop('categories')
        book = Book.objects.create(**validated_data)
        for author_data in authors_data:
            Author.objects.create(book=book, **author_data)
        for category_data in categories_data:
            Category.object.create(book=book, **category_data)
        return book