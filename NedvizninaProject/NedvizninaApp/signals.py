from .models import *
from django.dispatch import receiver
from django.db.models.signals import pre_save

@receiver(pre_save, sender=RealEstate)
def increment_total_sales_agent(sender, instance, **kwargs):
    if not instance.id:
        return
    old_instance = sender.objects.get(id=instance.id)
    if old_instance:
        if old_instance.isSold != instance.isSold:
            agents_real_estante = AgentRealEstate.objects.filter(real_estate=old_instance).all()
            for ar in agents_real_estante:
                agent = ar.agent
                agent.total_sales +=1
                agent.save()

