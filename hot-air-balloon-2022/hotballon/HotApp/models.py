from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#За секој балон се чуваат типот на балонот, име на производителот на балонот и максимален
#дозволен број на патници во балонот

class Ballon(models.Model):
    tip = models.CharField(max_length=50, blank=True, null=True)
    imeNaProizveduvac = models.CharField(max_length=50, blank=True, null=True)
    maxPatnici = models.IntegerField(blank=True, null=True)


#За секој пилот се цуваат неговотомиме и презиме, година на раѓање, вкупно часови на лет и чин
#кој го има во компанијата
class Pilot(models.Model):
    ime = models.CharField(max_length=50, blank=True, null=True)
    prezime = models.CharField(max_length=50, blank=True, null=True)
    godinaNaRagjanje = models.CharField(max_length=50, blank=True, null=True)
    vkupnoCasoviNaLet = models.IntegerField(blank=True, null=True)
    cinVoKompanijata = models.CharField(max_length=50, blank=True, null=True)

#а секоја авиокомпанија се чува нејзиното име, година на основање и информација дали лета надвор од Европа или не
class AvioKompanija(models.Model):
    ime = models.CharField(max_length=50, blank=True, null=True)
    godinaNaOsnovanje= models.IntegerField(blank=True, null=True)
    LetanadvorOdEvropa = models.BooleanField(blank=True, null=True)

class AvioKompanijaPilot(models.Model):
    aviokompanija = models.ForeignKey(AvioKompanija, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)

#Сложен модел, последен да се напише - има релации
#Секој лет се карактеризира со задолжителна шифра, име на кој аеродром полетува и на кој аеродром слетува
#корисник кој го креирал летот, фотографија за летот, инфо со кој балон се изведува летот
#пилот на летот и авиокомпанија која го реализира летот.
class Let(models.Model):
    id = models.AutoField(primary_key=True)
    sifra = models.CharField(max_length=50, blank=True, null=True)
    aerodromPoletuva = models.CharField(max_length=50, blank=True, null=True)
    aerodromSletuva = models.CharField(max_length=50, blank=True, null=True)
    kreator = models.ForeignKey(User, on_delete=models.CASCADE)
    fotografija = models.ImageField(upload_to = 'flights/', blank=True, null=True)
    balon = models.ForeignKey(Ballon, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    aviokompanija = models.ForeignKey(AvioKompanija, on_delete=models.CASCADE)
