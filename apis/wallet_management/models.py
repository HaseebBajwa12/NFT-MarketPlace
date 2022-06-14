from accounts.models import User
from django.db import models
from django.contrib.admin.models import LogEntry



class Wallet(models.Model):
    user = models.ForeignKey(User, related_name="user_wallet", on_delete=models.CASCADE)
    current_balance = models.FloatField(default=0)
    wallet_address = models.TextField(null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} : {self.wallet_address}"

class WalletTransaction(models.Model):
    wallet= models.OneToOneField(Wallet, related_name="wallet_transaction", on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)

    choices = [
        ("pay", "Pay"),
        ("deposit", "Deposit"),
        ("received", "Received")
    ]
    transaction_type = models.TextField(max_length=40, choices=choices, blank=False, null=False)
    transaction_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

