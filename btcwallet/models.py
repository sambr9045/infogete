from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    accountNumber = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.accountNumber)


class used_address(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    walletnumber = models.ForeignKey(Wallet, default=None, on_delete=models.CASCADE)
    btcaddress = models.CharField(max_length=250, default=None, null=None)
    amount = models.FloatField(
        default=None,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.btcaddress)
