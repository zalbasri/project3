from django.db import models
from django.contrib.auth.models import User


# for creating a regular pizza with a name and 2 prices based on side
class RegularPizza(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    # function for string representation of the pizza
    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"


# for creating a sicilian pizza with a name and 2 prices based on side
class SicilianPizza(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"


# for creating a topping
class Topping(models.Model):
    name = models.CharField(max_length=60, unique = True)

    def __str__(self):
        return self.name


# for creating a sub with a name and 2 prices based on side
class Sub(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}" # {self.toppings}


# for creating a pasta with a name and a price
class Pasta(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"


# for creating a salad with a name and a price
class Salad(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price}"


# for creating a dinner platter with a name and 2 prices
class DinnerPlatter(models.Model):
    name = models.CharField(max_length=60, unique = True)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.price_small} {self.price_large}"


# for creating an item in the virtual cart thaht belongs to a specific user
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=100) # contains every detail about the item ordered
    price = models.DecimalField(max_digits=4, decimal_places=2) # total price (with add ons)

    def __str__(self):
        return f"{self.user} {self.name} {self.price}"


# for creating orders in the database. Each order belongs to a user, has items and a total
# price and the superuser can update the status
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    items = models.TextField()
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    status = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.user} {self.status} {self.total} {self.items}"