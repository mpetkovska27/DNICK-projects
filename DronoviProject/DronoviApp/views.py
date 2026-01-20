from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
# Create your views here.

def index(request):
    






























def index(request): # почетна страна - листа на дронови
    # Земаме уникатни типови на дронови
    tipovi = Dron.objects.values_list('tip', flat=True).distinct()

    # Групираме во речник { 'Тип1': [дрон1, dрон2], 'Тип2': [дрон3] }
    grupirani_dronovi = {}
    for t in tipovi:
        grupirani_dronovi[t] = Dron.objects.filter(tip=t)

    return render(request, 'index.html', {'grupirani_dronovi': grupirani_dronovi})

def dron_details(request, dron_id): #страна за детали на дрон по id
    dron = get_object_or_404(Dron, id=dron_id)
    # Ги прикажуваме сите резервации за овој дрон
    rezervacii = Rezervacija.objects.filter(dron=dron)

    return render(request, 'dron_details.html', {'dron': dron,'rezervacii': rezervacii})

def add_rezervacija(request):
    if request.method == 'POST':
        form = RezervacijaForm(request.POST)
        if form.is_valid():
            rezervacija = form.save(commit=False)
            # Автоматски го доделуваме пилотот (најавениот корисник)
            rezervacija.odgovoren = Pilot.objects.get(user=request.user)
            rezervacija.save()
            return redirect('index')
    else:
        form = RezervacijaForm()
    return render(request, 'form.html', {'form': form})
