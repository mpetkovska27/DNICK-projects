from django.shortcuts import render, redirect
from .forms import *
from CakeApp.models import Cake, CustomUser


# Create your views here.
def index(request):
    cakes = Cake.objects.all()
    return render(request, 'index.html', {'cakes': cakes})

def add_cake(request):
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = CakeForm()
    return render(request, 'add.html', context={'form': form})