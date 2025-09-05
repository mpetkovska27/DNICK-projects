from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    contact = models.CharField(blank=True, null=True, max_length=100)
    is_baker = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Cake(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    price = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cakes/')
    baker = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


