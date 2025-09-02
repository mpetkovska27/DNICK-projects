from django.shortcuts import render
from BooksApp.models import *
from django.db.models import Q, Avg
from .forms import *
# Create your views here.

def book_list(request):
    total_books = Book.objects.count()
    avg_books = Book.objects.aggregate(Avg('publisher_year'))
    books = Book.objects.order_by('-publisher_year')[:10]
    filtered_books = Book.objects.filter(Q(publisher_year__gte=2010) & Q(author__name__startswith='M'))
    return render(request, 'book_list.html', {'books':books, 'total_books':total_books, 'avg_books':avg_books, 'filtered_books':filtered_books}, )

def create_book(request): #ednas da se izrenderira i ednas za da se kreira formata
    if request.method == 'POST': #post e method koga se kreira kniga
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        return book_list(request)
    else:
        form = BookForm()
    return render(request, 'createbook.html', {'form': form})




        #get e method koga sakame da ja izrenderirame samata strana
#post - kreira strana | get - ja prikazuva formata