from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
# Create your views here.

def index(request):
    tipovi = Dron.objects.values_list('tip', flat=True).distinct()
    grupirani_tipovi = {}

    for tip in tipovi:
        grupirani_tipovi[tip] = Dron.objects.filter(tip = tip)
    return render(request, 'index.html', {'grupirani_tipovi': grupirani_tipovi})

def dron_details(request, dron_id):
    dron = get_object_or_404(Dron, pk=dron_id)

    rezervacii = Rezervacija.objects.filter(dron = dron).all()

    return render(request, 'dron_details.html', {'dron':dron, 'rezervacii':rezervacii})

def add_rezervacija(request):
    if request.method == 'POST':
        form = RezervacijaForm(request.POST)
        if form.is_valid():
            rezervacija = form.save(commit=False)
            rezervacija.odgovoren = Pilot.objects.filter(user=request.user)
            rezervacija.save()
            return redirect('index')
    else:
        form = RezervacijaForm()
    return render(request, 'form.html', {'form':form})
