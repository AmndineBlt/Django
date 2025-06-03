from django.contrib import admin
from .models import Book, Review, UserList, ListEntry

# Book admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'page_count', 'rating', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('created_at',)

# Review admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating', 'created_at')

# UserList admin
@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('name',)
    search_fields = ('user__username',)

# ListEntry admin
@admin.register(ListEntry)
class ListEntryAdmin(admin.ModelAdmin):
    list_display = ('user_list', 'book', 'added_at')
    search_fields = ('user_list__user__username', 'book__title')
    list_filter = ('added_at',)