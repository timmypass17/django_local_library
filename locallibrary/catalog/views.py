from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Generate counts for genres and books that contain a particular word (case insensitive)
    num_demon_books = Book.objects.filter(title__icontains="demon").count()
    num_demon_instances_available = BookInstance.objects.filter(book__title__icontains="demon").count
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books': num_books,
        'num_demon_books': num_demon_books,
        'num_demon_instances_available': num_demon_instances_available
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)