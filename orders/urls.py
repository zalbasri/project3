from django.urls import path
from . import views

# creates paths the user can access
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:sub_id>", views.sub, name="sub"),
    path("<int:sub_id>/add_sub", views.add_sub, name="add_sub"),
    path("cart", views.cart_view, name="cart"),
    path("add_pasta", views.add_pasta, name="add_pasta"),
    path("add_salad", views.add_salad, name="add_salad"),
    path("add_platter", views.add_platter, name="add_platter"),
    path("add_regular", views.add_regular, name="add_regular"),
    path("add_sicilian", views.add_sicilian, name="add_sicilian"),
    path("order", views.order, name="order"),
    path("confirmation", views.confirmation, name="confirmation"),
    path("orders", views.order_view, name="orders")
]
