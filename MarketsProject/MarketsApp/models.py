from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Market(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    user_added = models.ForeignKey(User, on_delete=models.CASCADE)
    open_hours_from = models.TimeField(blank=True, null=True)
    open_hours_to = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    EMBG = models.CharField(max_length=12, unique=True, blank=True, null=True)
    user_added = models.ForeignKey(User, on_delete=models.CASCADE, )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"

class ContactInfo(models.Model):
    street = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

class Product(models.Model):
    TYPE_CHOICES = [
        ('Food', 'Food'),
        ('Drink', 'Drink'),
        ('Bakery', 'Bakery'),
        ('Cosmetic', 'Cosmetic'),
        ('Hygiene', 'Hygiene'),
    ]
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, )
    isHomemade = models.BooleanField(default=False)
    code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class MarketProduct(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #Достапна колицина во маркетите
    quantity = models.PositiveIntegerField(blank=True, null=True)