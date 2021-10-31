from django.contrib import admin
from .models import Book, Author, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

admin.site.register([
    Author,
    Category,
    ])