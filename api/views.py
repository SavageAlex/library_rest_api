import requests
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
import io

from .serializers import BookSerializer, CreateUpdateBookFromApiBookSerializer
from .models import Book, Author

class BookFilter(filters.FilterSet):

    class Meta:
        model = b=Book
        fields = ['title', 'authors', 'categories', 'average_rating', 'ratings_count',]

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    
    def get_queryset(self):
        queryset = Book.objects.all()
        print(self.request.query_params)
        sort = self.request.query_params.get('sort')
        author_list = self.request.query_params.getlist('author')
        published_date = self.request.query_params.get('published_date')
        if sort:
            queryset = queryset.order_by(sort)
        elif author_list:
            print('author_list: ', author_list)
            author_id_list = []
            for author in author_list:
                print('author: ', author)
                author_obj = Author.objects.filter(author_name=author)
                author_exists = author_obj.first()
                print('author_exists: ', author_exists)
                if author_exists is not None:
                    author_id_obj = author_obj.values('pk')
                    author_id = author_id_obj[0]['pk']
                    print('author_id: ', author_id)
                    author_id_list.append(author_id)
                    print('author_id_list: ', author_id_list)
            queryset = queryset.filter(authors__in=author_id_list).distinct()
        elif published_date:
            print(published_date)
            queryset = queryset.filter(published_date__year=published_date).distinct()

        return queryset

class CreateUpdateBookView(APIView):
    
    def post(self, request, format=None):
        body = self.request.query_params.dict()
        try:
            endpoint='https://www.googleapis.com/books/v1/volumes'
            r = requests.get(endpoint, params=body)
            r.raise_for_status()
            python_data = r.json()
            print(type(python_data))
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        book_list = python_data['items']
        i = 1
        
        def make_book_dict(book_dict, key, value):
            if value:
                book_dict[key] = value
            else:
                book_dict[key] = None
            return book_dict
        
        i=1
        book_list_of_dict = []
        for book in book_list:
            print(i)
            book_dict={}
            make_book_dict(book_dict, 'id', book['id'])
            make_book_dict(book_dict, 'title', book['volumeInfo'].get('title'))
            authors = book['volumeInfo'].get('authors')
            if authors:
                author_lsit = []
                for author in authors:
                    authors_dict = {}
                    authors_dict['author_name'] = author
                    author_lsit.append(authors_dict)
                book_dict['authors'] = author_lsit
            else:
                book_dict['authors'] = []
            make_book_dict(book_dict, 'publishedDate', book['volumeInfo'].get('publishedDate'))
            categories = book['volumeInfo'].get('categories')
            if categories:
                category_lsit = []
                for category in categories:
                    categories_dict = {}
                    categories_dict['category_name'] = category
                    category_lsit.append(categories_dict)
                book_dict['categories'] = category_lsit
            else:
                book_dict['categories'] = []
            book_dict['averageRating'] = book['volumeInfo'].get('averageRating', 0.0)
            book_dict['ratingsCount'] = book['volumeInfo'].get('ratingsCount', 0)
            if book['volumeInfo'].get('imageLinks'):
                make_book_dict(book_dict, 'thumbnail', book['volumeInfo']['imageLinks'].get('thumbnail'))
            else:
                book_dict['thumbnail'] = None
            book_list_of_dict.append(book_dict)
            print(book_dict)
            i += 1

        serializer = CreateUpdateBookFromApiBookSerializer(data=book_list_of_dict, many=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)