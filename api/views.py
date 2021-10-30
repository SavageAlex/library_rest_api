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

from .serializers import BookSerializer
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

class BookView(generics.ListCreateAPIView): # ListAPIView
    model = Book
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'authors', 'publishedDate', 'categories', 'averageRating', 'ratingsCount',)

    
    def get_queryset(self):
        queryset = Book.objects.all()
        published_date = self.request.query_params.get('published_date')
        sort = self.request.query_params.get('sort')
        author = self.request.query_params.get('author')
        if published_date:
            queryset = queryset.filter(publishedDate=published_date)
        elif author:
            queryset = queryset.filter(authors=author)
        elif sort:
            queryset = queryset.order_by(sort)
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
            data = r.json()
            print("Entire JSON response")
            print(data)
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        # content = JSONRenderer().render(jsonResponse)
        # stream = io.BytesIO(content)
        # data = JSONParser().parse(stream)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        

class DetailBookView(generics.RetrieveAPIView):
    pass