from django.contrib import admin
from .models import Book, Author, Category

admin.site.register([
    Book,
    Author,
    Category,
    ])