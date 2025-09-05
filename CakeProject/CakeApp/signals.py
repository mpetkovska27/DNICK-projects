import random
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import *


@receiver(pre_delete, sender=CustomUser)
def reasign_cakes(sender,instance, **kwargs):
    other_bakers = CustomUser.objects.exclude(id=instance.id).filter(is_baker=True)
    cakes = Cake.objects.filter(baker=instance)

    for cake in cakes:
        new_baker = random.choice(other_bakers)
        cake.baker = new_baker
        cake.save()