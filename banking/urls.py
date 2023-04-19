from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("loans/", views.loans, name="loans"),

    # APIs

    path("deposit/", views.deposit, name="deposit")


]
