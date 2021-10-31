from django.http.response import JsonResponse
import requests
from requests.exceptions import HTTPError
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
import io

from .serializers import BookSerializer, CreateUpdateBookFromApiBookSerializer
from .models import Book, Author

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'authors', 'published_date', 'categories', 'average_rating', 'ratings_count',)
    
    def get_queryset(self):
        queryset = Book.objects.all()
        print(self.request.query_params)
        sort = self.request.query_params.get('sort')
        author = self.request.query_params.getlist('author')
        print(author)
        if sort:
            queryset = queryset.order_by(sort)
        elif author:
            queryset = queryset.filter(authors__in=author).distinct()
        return queryset

class CreateUpdateBookView(APIView):
    # parser_class = JSONParser

    # def fetch_books_endpoint(self, request):
    #     body = self.request.query_params.dict()
    #     try:
    #         response = req.request(method='get', url='https://www.googleapis.com/books/v1/volumes', params=body)
    #         response.raise_for_status()
    #         jsonResponse = response.json()
    #         print("Entire JSON response")
    #         print(jsonResponse)
    #     except HTTPError as http_err:
    #         print(f'HTTP error occured: {http_err}')
    #     except Exception as err:
    #         print(f'Other error occured: {err}')
    #     request=jsonResponse
    #     return request

    def post(self, request, format=None):
        body = self.request.query_params.dict()
        try:
            endpoint='https://www.googleapis.com/books/v1/volumes'
            r = requests.get(endpoint, params=body)
            r.raise_for_status()
            python_data = r.json()
            print(type(python_data))
            # print("Entire JSON response")
            # print(python_data)
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        # content = JSONRenderer().render(jsonResponse)
        # stream = io.BytesIO(content)
        # data = JSONParser().parse(stream)
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
            make_book_dict(book_dict, 'averageRating', book['volumeInfo'].get('averageRating'))
            make_book_dict(book_dict, 'ratingsCount', book['volumeInfo'].get('ratingsCount'))
            if book['volumeInfo'].get('imageLinks'):
                make_book_dict(book_dict, 'thumbnail', book['volumeInfo']['imageLinks'].get('thumbnail'))
            else:
                book_dict['thumbnail'] = None
            book_list_of_dict.append(book_dict)
            print(book_dict)
            i += 1

        serializer = CreateUpdateBookFromApiBookSerializer(data=book_list_of_dict, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)