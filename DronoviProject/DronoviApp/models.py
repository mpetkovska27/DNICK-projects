from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


# Create your models here.
class Dron (models.Model):
    STATUS_CHOISES = [
        ('D', 'dostapen'),
        ('R', 'rezeriran'),
        ('S', 'servis'),
    ]
    TIP_CHOISES = [
        ('K', 'kinematski'),
        ('F', 'fvp'),
        ('I', 'industtriski'),
    ]
    seriski_broj = models.CharField(max_length=50)
    opis = models.TextField()
    vremetraenje = models.PositiveIntegerField()
    fotografija = models.ImageField(upload_to='photos/', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOISES)
    tip = models.CharField(max_length=1, choices=TIP_CHOISES)
    kompanija = models.CharField(max_length=50)
    def __str__(self):
        return self.seriski_broj

class Pilot (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    br_rezervacii = models.PositiveIntegerField()
    isActive = models.BooleanField()
    user = OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Rezervacija(models.Model):
    TERMIN_CHOISES = [
        ('U', 'utro'),
        ('P', 'popladne'),
        ('V', 'vecer'),
    ]
    STATUS_CHOISES = [
        ('C', 'cekanje'),
        ('A', 'aktivna'),
        ('Z', 'zavrshena'),
    ]
    datum = models.DateField()
    termin = models.CharField(max_length=1, choices=TERMIN_CHOISES)
    zabeleshka = models.TextField()
    kod = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=STATUS_CHOISES)
    odgovoren = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    dron = models.ForeignKey(Dron, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('dron', 'datum', 'termin')
    def __str__(self):
        return f'{self.dron} {self.datum} {self.termin}'

class PilotRezervacija(models.Model):
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    rezervacija = models.ForeignKey(Rezervacija, on_delete=models.CASCADE)



