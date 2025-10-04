from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Generate counts for genres and books that contain a particular word (case insensitive)
    num_demon_books = Book.objects.filter(title__icontains="demon").count()
    num_demon_instances_available = BookInstance.objects.filter(book__title__icontains="demon").count
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books': num_books,
        'num_visits': num_visits,
        'num_demon_books': num_demon_books,
        'num_demon_instances_available': num_demon_instances_available
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Using class-based generic views, Djanjo automatically looks for template <app_label>/<model_name>_list.html
# app_label: "catalog"
# model_name = "Book"
# So Django will look for: catalog/templates/catalog/book_list.html
# Or you can specific explicity using template_name
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='demon')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user) # filter book instances borrowed by current user
            .filter(status__exact='o')  # filter by "on loan" status
            .order_by('due_back')   # order by "due_back"
        )
    
class LoanedBooksListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(status__exact='o')  # filter by "on loan" status
            .order_by('due_back')   # order by "due_back"
        )