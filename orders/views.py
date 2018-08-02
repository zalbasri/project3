from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm #login form
from orders.forms import RegisterationForm # registeration form created
from decimal import Decimal # to calculate the prices in decimal
# imports all the models
from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter, Cart, Order

# menu page
def index(request):

    # gets all the menu items from the database
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


# register view
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def register(request):
    if request.method == 'POST':
        # gets the filled registration form that's in the html
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned_data makes sure it doesn't have thing that could be harmful
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

        # if input is invalid
        else:
            context = {
                'form': RegisterationForm(),
                'msg': "please fill the requirements"
            }
            return render(request, 'orders/register.html', context)

    # if request method is get, sends an non-filled regestration form
    else:
        form = RegisterationForm()

        context = {
            'form': form
        }
        return render(request, 'orders/register.html', context)


# logs the user in
# https://www.youtube.com/watch?v=XMgF3JwKzgs
def login_view(request):
    if request.method == 'POST':
        # gets the filled login form from the html
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    # if request method is get, sends an non-filled login form
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'orders/login.html', context)


# logs the user out & redirects to menu page
def logout_view(request):
    logout(request)
    return redirect('index')


# sends data for each sub in the sub's page
def sub(request, sub_id):
    try:
        # gets the sub with the requested id
        sub = Sub.objects.get(pk = sub_id)
    except Sub.DoesNotExist:
        raise Http404("Sub does not exist.")

    # by default each sub doesn't have additional toppings and has a small size option
    toppings = False
    small = True

    # if sub is Steak & Cheese, it has additional toppings
    if sub_id == 10:
        toppings = True

    # if sub is Sausage, Peppers & Onions, it doesn't have a small option
    if sub_id == 11:
        small = False

    context = {
        "sub": sub,
        "toppings": toppings,
        "small": small
    }
    return render(request, "orders/sub.html", context)


# gets the sub the user selected and adds it to their cart
def add_sub(request, sub_id):
    try:
        size = request.POST["size"]
        sub = Sub.objects.get(pk = sub_id)

        if size == 'small':
            price = sub.price_small

        elif size == 'large':
            price = sub.price_large

        name = sub.name + ' ' + size

        cheese = request.POST["cheese"]

        if cheese == 'with extra cheese':
            price += Decimal(0.5)
            name += ' ' + cheese


        # is sub is Steak & Cheese check for extra toppings
        if sub_id == 10:
            mushrooms = request.POST["mushrooms"]
            if mushrooms == 'with mushrooms':
                price += Decimal(0.5)
                name += ' ' + mushrooms
            green_peppers = request.POST["green_peppers"]
            if green_peppers == 'with green peppers':
                price += Decimal(0.5)
                name += ' ' + green_peppers
            onions = request.POST["onions"]
            if onions == 'with onion':
                price += Decimal(0.5)
                name += ' ' + onions


    except KeyError:
        return render(request, "orders/sub.html", {"message": "No selection."})
    except Sub.DoesNotExist:
        return render(request, "orders/sub.html", {"message": "No sub."})

    # gets the current user
    user = request.user
    # adds item to cart
    cart = Cart.objects.create(user=user, name=name, price=price)

    return redirect('index')


# renders the cart items to the html page
def cart_view(request):
    user = request.user
    # gets all the items in the cart model where the user is the current user
    items = Cart.objects.filter(user=user).values()
    context = {
        "items": items,
        "exists": items.exists()
    }
    return render(request, "orders/cart.html", context)


# gets the pasta the user selected and adds it to their cart
def add_pasta(request):
    try:
        pasta_id = int(request.POST["pasta"])
        pasta = Pasta.objects.get(pk = pasta_id)
    except Pasta.DoesNotExist:
        raise Http404("Pasta does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=pasta.name, price=pasta.price)

    return redirect('index')


# gets the salad the user selected and adds it to their cart
def add_salad(request):
    try:
        salad_id = int(request.POST["salad"])
        salad = Salad.objects.get(pk = salad_id)
    except Salad.DoesNotExist:
        raise Http404("Salad does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=salad.name, price=salad.price)

    return redirect('index')


# gets the dinner platter the user selected and adds it to their cart
def add_platter(request):
    try:
        platter_id = int(request.POST["dinner_platter"])
        platter = DinnerPlatter.objects.get(pk = platter_id)
        # gets the size the user selected
        size = request.POST["size"]

        if size == 'small':
            price = platter.price_small

        elif size == 'large':
            price = platter.price_large

    except DinnerPlatter.DoesNotExist:
        raise Http404("Dinner platter does not exist.")

    user = request.user
    cart = Cart.objects.create(user=user, name=platter.name + ' ' + size, price=price)

    return redirect('index')


# gets the regular pizza the user selected and adds it to their cart
def add_regular(request):
    topping1 = request.POST["topping1"]
    topping2 = request.POST["topping2"]
    topping3 = request.POST["topping3"]
    topping4 = request.POST["topping4"]
    size = request.POST["size"]

    # name of the pizza
    name = ""
    # tracks the number of toppings to calculate the price
    numToppings= 0

    # checks the input for the topping selection and adds it to the pizza
    # name if the input is not 'no topping'
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

    # if the pizza has toppings it's not cheese pizza
    if numToppings != 0:
        name = size + " regular pizza with " + name

    else:
        name = size + " regular cheese pizza"


    # gets the pizza type depending on the number of toppings
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


# gets the sicilian pizza the user selected and adds it to their cart
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
        pizza = SicilianPizza.objects.get(name='1 item')

    elif numToppings == 2:
        pizza = SicilianPizza.objects.get(name='2 items')

    elif numToppings == 3:
        pizza = SicilianPizza.objects.get(name='3 items')

    elif numToppings == 4:
        pizza = SicilianPizza.objects.get(name='Special')

    if size == 'small':
        price = pizza.price_large

    elif size == 'large':
        price = pizza.price_large


    user = request.user
    cart = Cart.objects.create(user=user, name=name, price=price)

    return redirect('index')


# order page
def order(request):
    total = 0 # total price of order
    order_items = "" # items in the cart
    user = request.user
    items = Cart.objects.filter(user=user).values()
    # iterates through each item in the user's cart
    for item in items:
        price = item['price']
        name = item['name']
        order_items += name + ' ' # adds each item's name to the order string
        total += price # adds each item to the total

    context = {
        "items": items,
        "total": total
    }

    return render(request, 'orders/order.html', context)


# order is actually submitted
def confirmation(request):
    total = 0
    order_items = ""
    user = request.user
    items = Cart.objects.filter(user=user).values()
    for item in items:
        price = item['price']
        name = item['name']
        order_items += name + ', '
        total += price

    # adds the order to the database, includes the user, the items ordered and the total
    # default order status is pending
    order = Order.objects.create(user=user, items=order_items, total=total, status="pending")
    cart = Cart.objects.filter(user=user).delete()

    return redirect('index')


# user can view all their orders
def order_view(request):
    user = request.user
    # gets all orders of the user
    orders = Order.objects.filter(user=user).values()
    context = {
        "orders": orders,
        "exists": orders.exists()
    }

    return render(request, 'orders/orders.html', context)