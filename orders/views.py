from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from orders.forms import RegisterationForm

from decimal import Decimal

from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter, Cart

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

        if cheese == 'with extra cheese':
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

    cart = Cart.objects.create(user=user, name=sub.name + ' ' + size, price=price)


    return redirect('index')


def cart_view(request):
    user = request.user
    context = {
        "items": Cart.objects.filter(user=user).values()
    }

    return render(request, "orders/cart.html", context)


def add_pasta(request):
    try:
        pasta_id = int(request.POST["pasta"])
        pasta = Pasta.objects.get(pk = pasta_id)
    except Pasta.DoesNotExist:
        raise Http404("Pasta does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=pasta.name, price=pasta.price)

    return redirect('index')


def add_salad(request):
    try:
        salad_id = int(request.POST["salad"])
        salad = Salad.objects.get(pk = salad_id)
    except Salad.DoesNotExist:
        raise Http404("Salad does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=salad.name, price=salad.price)

    return redirect('index')


def add_platter(request):
    try:
        platter_id = int(request.POST["dinner_platter"])
        platter = DinnerPlatter.objects.get(pk = platter_id)
        size = request.POST["size"]

        if size == 'small':
            price = platter.price_small

        elif size == 'large':
            price = platter.price_large

    except DinnerPlatter.DoesNotExist:
        raise Http404("Dinner platter does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=platter.name, price=price)

    return redirect('index')


def add_regular(request):
    topping1 = request.POST["topping1"]
    topping2 = request.POST["topping2"]
    topping3 = request.POST["topping3"]
    topping4 = request.POST["topping4"]
    size = request.POST["size"]

    name = ""
    numToppings= 0
    if topping1 != "no topping":
        numToppings += 1
        name += topping1

    if topping2 != "no topping":
        numToppings += 1
        name += ", " + topping2

    if topping3 != "no topping":
        numToppings += 1
        name += ", " + topping3

    if topping4 != "no topping":
        numToppings += 1
        name += ", " + topping4

    if numToppings != 0:
        name = size + " regular pizza with " + name

    else:
        name = size + " regular cheese pizza"


    if numToppings == 0:
        pizza = RegularPizza.objects.get(name='Cheese')

    elif numToppings == 1:
        pizza = RegularPizza.objects.get(name='1 topping')

    elif numToppings == 2:
        pizza = RegularPizza.objects.get(name='2 toppings')

    elif numToppings == 3:
        pizza = RegularPizza.objects.get(name='3 toppings')

    elif numToppings == 4:
        pizza = RegularPizza.objects.get(name='Special')

    if size == 'small':
        price = pizza.price_large

    elif size == 'large':
        price = pizza.price_large


    user = request.user
    cart = Cart.objects.create(user=user, name=name, price=price)

    return redirect('index')


def add_sicilian(request):
    topping1 = request.POST["topping1"]
    topping2 = request.POST["topping2"]
    topping3 = request.POST["topping3"]
    topping4 = request.POST["topping4"]
    size = request.POST["size"]

    name = ""
    numToppings= 0
    if topping1 != "no topping":
        numToppings += 1
        name += topping1

    if topping2 != "no topping":
        numToppings += 1
        name += ", " + topping2

    if topping3 != "no topping":
        numToppings += 1
        name += ", " + topping3

    if topping4 != "no topping":
        numToppings += 1
        name += ", " + topping4

    if numToppings != 0:
        name = size + " sicilian pizza with " + name

    else:
        name = size + " sicilian cheese pizza"


    if numToppings == 0:
        pizza = SicilianPizza.objects.get(name='Cheese')

    elif numToppings == 1:
        pizza = SicilianPizza.objects.get(name='1 topping')

    elif numToppings == 2:
        pizza = SicilianPizza.objects.get(name='2 toppings')

    elif numToppings == 3:
        pizza = SicilianPizza.objects.get(name='3 toppings')

    elif numToppings == 4:
        pizza = SicilianPizza.objects.get(name='Special')

    if size == 'small':
        price = pizza.price_large

    elif size == 'large':
        price = pizza.price_large


    user = request.user
    cart = Cart.objects.create(user=user, name=name, price=price)

    return redirect('index')


# def order(request):
#     user = request.user
#     items = Cart.objects.filter(user=user).values()
#     total = 0
#     for item in items:
#         total = item.price
#     context = {
#         "items": items
#         "total": total
#     }
#     return render(request, )
