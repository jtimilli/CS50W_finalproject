from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from .models import User, Account, Transactions

# Create your views here.


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
        account = Account.objects.create(user=user)
        account.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


@login_required()
def index(request):
    account = Account.objects.get(user=request.user)
    transactions = Transactions.objects.filter(
        account=account).order_by('-timestamp')
    return render(request, 'banking/homepage.html', {"account": account, "transactions": transactions})


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


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def deposit(request):
    if request.method == "POST":
        user = request.user

        deposit = request.POST.get("amount")

        if Decimal(deposit) > 0.01:
            try:
                account = Account.objects.get(user=user)
                account.balance = Decimal(account.balance) + Decimal(deposit)
                account.save()
                transaction = Transactions.objects.create(
                    account=account, transactions=f"Deposited ${deposit} amount to your account")
                transaction.save()
                print(account.balance)
            except Account.DoesNotExist:
                HttpResponse("Something went wrong")
        else:
            return HttpResponse("Invalid amount-amount must be over 1 penny")
        return HttpResponseRedirect(reverse(index))
    else:
        pass


def loans(request):
    return render(request, "banking/loans.html")

# TODO: Create save feature for banking transactions
