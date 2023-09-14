import csv
import requests
import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal
from django.utils.timezone import localtime

from .models import User, Account, Transactions, StockPortfolio
from .secrets import api_key
from .functions import searchStock, searchAccount, getNews


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


def load_landing(request):
    return render(request, 'banking/landingpage.html')


@login_required()
def index(request):
    account = Account.objects.get(user=request.user)
    data = getNews('')
    transactions = Transactions.objects.filter(
        account=account).order_by('-timestamp')
    return render(request, 'banking/homepage.html', {"account": account, "transactions": transactions, "data": data})


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
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
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


def download_transactions(request):
    account = Account.objects.get(user=request.user)
    transactions = Transactions.objects.filter(
        account=account).order_by("-timestamp")

    # Create CSV file
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=bankstatement.csv"

    # Define fieldnames for CSV
    fieldnames = ['transaction_date',
                  'transaction']  # Example fieldnames

    # Write transactions to CSV
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()  # Write CSV header row
    for transaction in transactions:
        formatted_timestamp = localtime(
            transaction.timestamp).strftime('%Y-%m-%d %H:%M')
        writer.writerow({
            'transaction_date': formatted_timestamp,
            'transaction': transaction.transactions

        })

    return response


def transfer_funds(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        receiver_account_number = request.POST.get(
            "receiverAccountNumber", None).upper()
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


@csrf_exempt
def checkForReceiver(request):
    if request.method == "POST":
        account = json.loads(request.body)['accountNumber'].lower()
        list_account = Account.objects.all().order_by("account_number")
        print(list_account)
        is_account = searchAccount(list_account, account)
        if is_account:
            return JsonResponse({"found": "account active"})
        else:
            return JsonResponse({"error": "No account with that number"})


def load_investPage(request):
    return render(request, "banking/investing.html")


def loadUserStock(request):
    account = Account.objects.get(user=request.user)
    api_key_value = api_key

    try:
        list_stocks = StockPortfolio.objects.filter(account=account)
        list_stocks = [obj.stock for obj in list_stocks]
        if len(list_stocks) == 0:
            return JsonResponse({}, safe=False)
        if len(list_stocks) > 1:
            symbols = ','.join(list_stocks)
        else:
            print(list_stocks)
            symbols = list_stocks[0] if list_stocks else []
    except StockPortfolio.DoesNotExist:
        symbols = ""

    # Call API
    url = f"https://api.twelvedata.com/time_series?symbol={symbols}&apikey={api_key}&interval=1min"
    response = requests.get(url).json()
    stocks_data = []

    # If user owns only one stock
    if ',' not in symbols:
        lastest_price = response.get('values', [])[0].get('close', {})
        quantity = StockPortfolio.objects.get(
            account=account, stock=symbols).quantity
        stocks_data.append(
            {'ticker': list_stocks, 'price': lastest_price, "quantity": quantity})

    else:
        # For each ticker, get that object and it's value from the response add new object to array, return array
        for ticker in list_stocks:
            stock_values = response.get(ticker, {}).get('values', [])
            if stock_values:
                latest_price = stock_values[0].get('close', '')
                quantity = StockPortfolio.objects.get(
                    account=account, stock=ticker).quantity
                stocks_data.append(
                    {'ticker': ticker, 'price': latest_price, "quantity": quantity})
    return JsonResponse(stocks_data, safe=False)


def loadStock(request, symbol):
    response = searchStock(symbol)
    if response["status"] == 200:
        return JsonResponse(response["data"], status=response["status"], safe=False)
    else:
        return JsonResponse({"Error": response["error"]}, status=response["status"])


@csrf_exempt
def tradeStocks(request):
    if request.method == "POST":
        user = request.user
        account = Account.objects.get(user=user)
        data = json.loads(request.body)

        quantity, trade_type, symbol, price = Decimal(
            data["quantity"]), data["type"], data["symbol"], Decimal((data["price"]))

        # Try getting user's portfolio
        try:
            users_portfolio = StockPortfolio.objects.get(
                account=account, stock=symbol)
        except StockPortfolio.DoesNotExist:
            users_portfolio = None

        # If quantity is 0
        if quantity < 1:
            return JsonResponse({'error': "Must buy or sell at least one stock"})

        # Handle buying the stock
        if trade_type == "buy":
            cost = quantity * price

            if Decimal(account.balance - cost) < 0:
                return JsonResponse({"error": f"Your balance of ${account.balance} is not enough to make this trade (${cost})"}, status=400)

            # If user does not own any of the stock
            if users_portfolio == None:
                users_portfolio = StockPortfolio.objects.create(
                    account=account, stock=symbol, quantity=quantity)
            else:
                users_portfolio.quantity = users_portfolio.quantity + quantity

            # Add transaction
            user_transaction = Transactions.objects.create(
                account=account, transactions=f"Purchased {quantity} {symbol} stock(s) @ ${price} each")

            user_transaction.save()
            users_portfolio.save()
            account.balance = account.balance - cost
            account.save()
            return JsonResponse({"success": "You have successfully purchased stock"}, status=200)

        # Handle selling the stock
        if trade_type == "sell":
            if users_portfolio == None:
                return JsonResponse({"error": "You don't own any of this stock to sell"}, status=200)

            if users_portfolio.quantity < quantity:
                return JsonResponse({"error": "You can't sell more stocks than you own"}, status=200)

            cost = quantity * price
            account.balance = account.balance + cost
            users_portfolio.quantity = users_portfolio.quantity - quantity
            users_portfolio.save()

            if users_portfolio.quantity == 0:
                users_portfolio.delete()

             # Add transaction
            user_transaction = Transactions.objects.create(
                account=account, transactions=f"Sold {quantity} {symbol} stock(s) @ ${price} each")

            user_transaction.save()
            account.save()
            return JsonResponse({"success": "You successfully sold the stock"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=200)
