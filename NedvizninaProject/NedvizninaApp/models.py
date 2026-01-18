from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField


# Create your models here.
class RealEstate(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    area = models.DecimalField(decimal_places=2, max_digits=10)
    date_published = models.DateField()
    photo = models.ImageField(upload_to='photos/')
    isReserved = models.BooleanField(default=False)
    isSold = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Agent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=50)
    total_sales = models.PositiveIntegerField()
    email = models.EmailField()
    user = OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AgentRealEstate(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

class Characteristic (models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    def __str__(self):
        return self.name

class CharacteristicRealEstate(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)



