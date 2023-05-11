from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

# Create your models here.


class User(AbstractUser):
    pass


class Account(models.Model):
    # Other fields for the Account model
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="account_holder")
    account_number = models.CharField(max_length=10, unique=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=25, null=True)

    unique_together = ["user", "account_number"]

    def save(self, *args, **kwargs):
        if not self.account_number:
            # Generate a random alphanumeric account number
            self.account_number = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.account_number


class Transactions(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transactions = models.CharField(max_length=64, null=True)
    timestamp = models.DateTimeField(auto_now=True)


class StockPortfolio(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10, unique=True)
    quantity = models.IntegerField()
