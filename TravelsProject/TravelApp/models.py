from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=100, null=True, blank=True)
    is_guide = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Travel(models.Model):
    destination = models.CharField(max_length=100, null=True, blank=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='travels/', null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f'{self.destination} - {self.price}'

