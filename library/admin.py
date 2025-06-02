from django.contrib import admin
from .models import Book

# Register the Book model in the admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'page_count', 'rating', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('created_at',)
