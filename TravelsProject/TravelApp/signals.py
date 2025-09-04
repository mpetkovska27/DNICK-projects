import random

from django.db.models.signals import  pre_delete
from django.dispatch import receiver
from .models import *

@receiver(pre_delete, sender=CustomUser)
def reasign_travels_post_delete(sender,instance, **kwargs):

    other_guids = list(CustomUser.objects.exclude(id=instance.id).filter(is_guide=True))
    travels = list(Travel.objects.filter(creator=instance))
    for travel in travels:
        new_creator = random.choice(other_guids)
        travel.creator = new_creator
        travel.save()
