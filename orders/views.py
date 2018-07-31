from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from orders.forms import RegisterationForm

from decimal import Decimal

from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter, Cart, Item

# Create your views here.
def index(request):
    context = {
        "regular_pizzas": RegularPizza.objects.all(),
        "sicilian_pizzas": SicilianPizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": DinnerPlatter.objects.all()
    }
    return render(request, "orders/index.html", context)


# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

    else:
        form = RegisterationForm()

        args = {'form': form}
        return render(request, 'orders/register.html', args)


# https://www.youtube.com/watch?v=XMgF3JwKzgs
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('index')


def sub(request, sub_id):
    try:
        sub = Sub.objects.get(pk = sub_id)
    except Sub.DoesNotExist:
        raise Http404("Sub does not exist.")

    toppings = False
    small = True

    if sub_id == 10:
        toppings = True

    if sub_id == 11:
        small = False

    context = {
        "sub": sub,
        "toppings": toppings,
        "small": small
    }
    return render(request, "orders/sub.html", context)


def add_sub(request, sub_id):
    try:
        size = request.POST["size"]
        sub = Sub.objects.get(pk = sub_id)

        if size == 'small':
            price = sub.price_small

        elif size == 'large':
            price = sub.price_large

        cheese = request.POST["cheese"]

        if cheese == 'with cheese':
            price += Decimal(0.5)

        if sub_id == 10:
            mushrooms = request.POST["mushrooms"]
            if mushrooms == 'with mushrooms':
                price += Decimal(0.5)
            green_peppers = request.POST["green_peppers"]
            if green_peppers == 'with green peppers':
                price += Decimal(0.5)
            onions = request.POST["onions"]
            if onions == 'with onion':
                price += Decimal(0.5)


    except KeyError:
        return render(request, "orders/sub.html", {"message": "No selection."})
    except Sub.DoesNotExist:
        return render(request, "orders/sub.html", {"message": "No sub."})

    user = request.user
    item = Item.objects.create(name= sub.name + ' ' + size, price=price)
    item.save()

    try:
        cart = Cart.objects.get(user=user)
        print(cart)
        cart.items.add(item)
        print(cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart.save()
        print(cart)
        cart.items.set(item)
        cart.save()
        print(Cart)

    return redirect('index')