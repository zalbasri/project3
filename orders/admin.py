from django.contrib import admin

from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter, Cart, Order

# registers models for admin (superuser) access
admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Cart)
admin.site.register(Order)