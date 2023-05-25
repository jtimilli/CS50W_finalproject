from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("loans/", views.loans, name="loans"),
    path("transfer/", views.transfer_funds, name="transfer"),
    path("invest/", views.load_investPage, name="invest_page"),
    path('landing/', views.load_landing, name="landing"),

    # APIs
    path("stock_info/<str:symbol>/", views.loadStock, name="stock_info"),
    path("deposit/", views.deposit, name="deposit"),
    path("userstocks/", views.loadUserStock, name="userstock"),
    path("download_csv/", views.download_transactions, name="download_csv"),
    path("trade/", views.tradeStocks, name="trade"),
    path("check_reciever_account", views.checkForReceiver, name="receiever_accoutn")

]
