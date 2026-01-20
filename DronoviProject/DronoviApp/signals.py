from urllib.request import Request

from django.db.models import Count
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

import DronoviApp
from .models import *

@receiver(pre_save, sender=Rezervacija)
def update_rezervacija(sender,instance, **kwargs):
    if not instance.pk:
        return
    old_instance = sender.objects.get(pk=instance.pk)
    if old_instance:
        if old_instance.status=='C' and instance.status=='A':
            pilotce = instance.odgovoren
            pilotce.br_rezervacii += 1
            pilotce.save()

            dronce = instance.dron
            if dronce.status=='D':
                dronce.status = 'R'
                dronce.save()
        if instance.status=='A' and instance.dron.status=='S':
            instance.status = 'C'
            instance.zabeleshka = "Dronot e na servis."

@receiver(pre_delete, sender=Dron)
def delete_dron(sender, instance, **kwargs):
    rezervaciicka = Rezervacija.objects.filter(dron=instance,status='C')
    if rezervaciicka.exists():
        zamena_dron = Dron.objects.filter(
            tip = instance.tip,
            status = 'D'
        ).exclude(id=instance.id).annotate(
            vkupno_rez = Count('rezervacija')
        ).order_by('vkupno_rez').first()
        if zamena_dron:
            for rez in rezervaciicka:
                rez.dron=zamena_dron
                rez.save()

