from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegularPizza(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"


class SicilianPizza(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"


class Topping(models.Model):
    name = models.CharField(max_length=60, unique = True)

    def __str__(self):
        return self.name


class Sub(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}" # {self.toppings}


class Pasta(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"



class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return f"{self.user} {self.items}"