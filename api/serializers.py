from rest_framework import serializers
from .models import Book, Author, Category

class AuthorSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
         return value.author_name

    class Meta:
        model = Author
        fields = ['author_name',]

class CategorySerializer(serializers.ModelSerializer):

    def to_representation(self, value):
        return value.category_name

    class Meta:
        model = Category
        fields = ['category_name',]

class BookSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'published_date', 'categories', 'average_rating', 'ratings_count', 'thumbnail'] # representation must be published_date, avaerage_rating, ratings_count
        depth = 2

class CreateUpdateBookFromApiBookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    publishedDate = serializers.DateField(source='published_date', format="%Y", input_formats=["%Y-%m-%d", "%Y-%m", "%Y"], allow_null=True)
    averageRating = serializers.FloatField(source='average_rating', allow_null=True)
    ratingsCount = serializers.IntegerField(source='ratings_count', allow_null=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publishedDate', 'categories', 'averageRating', 'ratingsCount', 'thumbnail'] # representation must be published_date, avaerage_rating, ratings_count
        depth = 2

    def create(self, validated_data):
        book_id = validated_data.get('id', None)
        authors_data = validated_data.pop('authors')
        categories_data = validated_data.pop('categories')
        if book_id is not None:
            book = Book.objects.filter(id=book_id).first()
            if book is not None: # if book already exists
                book = Book.objects.filter(id=book_id)
                book.update(**validated_data) # update existing book
                book = Book.objects.get(id=book_id)                   
                for author_data in authors_data:
                    if author_data is not None:
                        author = Author.objects.filter(author_name=author_data.get('author_name')).first()
                        if author is None: # if author not exists
                            author = Author.objects.create(book=book, **author_data) # creating new author
                        book.authors.add(author)
                for category_data in categories_data:
                    if category_data is not None:
                        category = Category.objects.filter(category_name=category_data.get('category_name')).first()
                        if category is None:
                            category = Category.objects.create(book=book, **category_data)
                        book.categories.add(category)
            else:
                book = Book.objects.create(**validated_data) # create new book
                for author_data in authors_data:
                    if author_data is not None:
                        author = Author.objects.filter(author_name=author_data.get('author_name')).first()
                        if author is None: # if author not exists
                            author = Author.objects.create(book=book, **author_data) # creating new author
                        book.authors.add(author)
                for category_data in categories_data:
                    if category_data is not None:
                        category = Category.objects.filter(category_name=category_data.get('category_name')).first()
                        if category is None:
                            category = Category.objects.create(book=book, **category_data)
                        book.categories.add(category)
        return book