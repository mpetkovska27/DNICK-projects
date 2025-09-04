from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.

def index(request):
    travels = Travel.objects.all()
    return render(request, 'index.html', {'travels': travels})

def add_travels(request):
    if request.method == 'POST':
        form = TravelForm(request.POST)
        if form.is_valid():
            form.save()
        return index(request)
    else:
        form = TravelForm()
        return render(request, 'add_destination.html', {'form': form})