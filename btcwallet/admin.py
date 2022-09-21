from django.contrib import admin
from . import models

# Register your models here.
class Wallet_(admin.ModelAdmin):
    model: models.Wallet
    list_display = ("accountNumber",)


admin.site.register(models.Wallet, Wallet_)


class usedAddress(admin.ModelAdmin):
    model: models.used_address
    list_display = ("user", "walletnumber", "btcaddress", "created_at")


admin.site.register(models.used_address, usedAddress)
