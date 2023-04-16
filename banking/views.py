from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import User

# Create your views here.

# TODO: Allow users to register and be redirected to index page


@csrf_exempt
def register(request):
    if request.method != "POST":
        return render(request, 'banking/register.html')

    if request.method == "POST":

        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure passwords match
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Ensure all fields are provided
        if not username or not first_name or not last_name or not email or not password or not confirm_password:
            message = "Please fill in all fields"
            return render(request, "banking/register.html", {"field_error": message})

        if password != confirm_password:
            message = "Password did not match"
            return render(request, "banking/register.html", {"password_error": message})

        # Try to create user
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            message = "Username already exists"
            return render(request, "banking/register.html", {"username_error": message})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))


@login_required
def index(request):
    return render(request, 'banking/homepage.html')


# TODO: Allow user to login
@csrf_exempt
def login_user(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "banking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "banking/login.html")


# TODO: Implement logout
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
