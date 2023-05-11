from django.contrib import admin
from .models import User, Account, StockPortfolio

# Register your models here.

admin.site.register(User)
admin.site.register(Account)
admin.site.register(StockPortfolio)
