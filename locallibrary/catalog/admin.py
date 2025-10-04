from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0  # remove default extra placeholders rows in inline view, just show our existing instances


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # Update layout of author detail view for admin site
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    # Add line listing of Book items to Author detail view
    inlines = [BooksInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # remove default extra placeholders rows in inline view, just show our existing instances


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    # Add line listing of Book instances to Book detail view
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    # Add filter option for admin site
    list_filter = ('status', 'due_back')

    # Section fields for admin site
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
