from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from orders.forms import RegisterationForm

from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter

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


