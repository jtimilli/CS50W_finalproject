from django.shortcuts import render
from django.http import HttpResponse
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

        # Ensure passwords match
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            message = "Password did not match"
            return render(request, "banking/register.html", {"password_error": message})

        # Check if user name exists
        try:
            name_exist = User.objects.get(username=username)
        except User.DoesNotExist:
            name_exist = None

        if name_exist == None:
            render(request, "banking/reguister.html",
                   {"username_error": message})

        else:
            return HttpResponse("Hello there")


@login_required
def index(request):
    return render(request, 'banking/homepage.html')

# TODO: Allow user to login


def login(request):
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "banking/login.html")

# TODO: Implement logout
