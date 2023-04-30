import csv
import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from .models import User, Account, Transactions
from .functions import get_stocks

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
        account_type = request.POST["account_type"]

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
        account = Account.objects.create(user=user, account_type=account_type)
        account.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


@login_required()
def index(request):
    account = Account.objects.get(user=request.user)
    stocks = get_stocks()
    transactions = Transactions.objects.filter(
        account=account).order_by('-timestamp')
    return render(request, 'banking/homepage.html', {"account": account, "transactions": transactions, "stocks": stocks})


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


@csrf_exempt
def deposit(request):
    if request.method == "POST":
        user = request.user

        deposit = json.loads(request.body).get("amount")

        if Decimal(deposit) > 0.01:
            try:
                account = Account.objects.get(user=user)
                account.balance = Decimal(account.balance) + Decimal(deposit)
                account.save()
                transaction = Transactions.objects.create(
                    account=account, transactions=f"Deposited ${deposit} amount to your account")
                transaction.save()
                return JsonResponse("Deposit cash succesfully")
            except Account.DoesNotExist:
                return JsonResponse("Something went wrong")
        else:
            return JsonResponse("Invalid amount-amount must be over 1 penny")
        # return HttpResponseRedirect(reverse(index))
    else:
        pass


def loans(request):
    return render(request, "banking/loans.html")

# TODO: edit columns and how timestamp is presented


def download_transactions(request):
    account = Account.objects.get(user=request.user)
    transactions = Transactions.objects.filter(account=account)

    # Create CSV file
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=bankstatement.csv"

    # Define fieldnames for CSV
    fieldnames = ['transaction_date',
                  'transaction_amount']  # Example fieldnames

    # Write transactions to CSV
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()  # Write CSV header row
    for transaction in transactions:
        writer.writerow({
            'transaction_date': transaction.timestamp,
            'transaction_amount': transaction.transactions

        })

    return response


def transfer_funds(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        receiver_account_number = request.POST.get(
            "receiverAccountNumber", None)
        transfer_amount = Decimal(request.POST.get("transferAmount", None))

        if account.account_number == receiver_account_number:
            return HttpResponse("Can't send money to yourself")

        if receiver_account_number != None and transfer_amount != None:
            # Check to see if user has enough money to send
            if account.balance < transfer_amount:
                return HttpResponse("You do not have enough to send that amount at the moment")

            # Check receiver's account number is a valid account
            try:
                receiver = Account.objects.get(
                    account_number=receiver_account_number)
                receiver.balance += transfer_amount
                account.balance -= transfer_amount
                receiver.save()
                account.save()
            except Account.DoesNotExist:
                return HttpResponse("No users with that account number")

            # Add transactions to the respective users' accounts
            receiver_transaction = Transactions.objects.create(
                account=receiver, transactions=f"You have recieve ${transfer_amount} from {account.user.first_name.capitalize()}")
            sender_transaction = Transactions.objects.create(
                account=account, transactions=f"You sent ${transfer_amount} to {receiver.user.first_name.capitalize()}")
            receiver_transaction.save()
            sender_transaction.save()
            return HttpResponseRedirect(reverse("index"))

        elif receiver_account_number == None:
            return HttpResponse("Must enter an account number")
        elif transfer_amount == None:
            return HttpResponse("Must enter an amount to send")

    else:
        return render(request, "banking/transfer.html", {"account": account})
