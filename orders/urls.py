from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:sub_id>", views.sub, name="sub"),
    path("<int:sub_id>/add_sub", views.add_sub, name="add_sub")
]
