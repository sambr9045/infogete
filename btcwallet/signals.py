from asyncio.windows_events import NULL
import numbers
from urllib import request
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from dashboard import models
from .btcWallet import BtcWallet
from dotenv import load_dotenv
import os
import threading
from dashboard.views import log_notification
from django.utils import timezone
from dateutil.relativedelta import *


load_dotenv()


@receiver(post_save, sender=models.transactions)
def transactionvalidator(sender, instance, created, **kwargs):
    if created:
        x = threading.Thread(
            target=thread_function,
            args=(instance,),
            daemon=True,
        )
        x.start()


def wallet():
    w = BtcWallet(os.getenv("BTCWALLETNAME"), os.getenv("BTCKEYPHRASE"))
    return w


def thread_function(instance):
    w = wallet()
    data = w.monitor(instance)
    if data[1][3] > 0:
        confirmation = data[1][2]
        balance = data[1][3]

        if data[0] == "renew":
            timestamp = NULL
            old_plan = models.suscriptions.objects.filter(user=instance.user).first()
            if old_plan.expired_on < timezone.now():
                timestamp = timezone.now()
            else:
                timestamp = old_plan.expired_on

            next_expiration_date = timestamp + relativedelta(months=+old_plan.periode)

            models.transactions.objects.filter(
                transactions_id=instance.transactions_id
            ).update(
                amount=balance, confirmation=confirmation, updated_at=timezone.now()
            )
            models.suscriptions.objects.filter(user=instance.user).update(
                paid=True, plan_active=True, expired_on=next_expiration_date
            )

            print("periode update successfully")
        else:
            models.transactions.objects.filter(
                transactions_id=instance.transactions_id
            ).update(
                amount=balance, confirmation=confirmation, updated_at=timezone.now()
            )
            models.suscriptions.objects.filter(user=instance.user).update(
                paid=True, plan_active=True, updated_at=timezone.now()
            )
            print("data plan newplan confirm ")
        print(data, "on signale side")
    else:
        try:
            models.suscriptions.objects.filter(user=instance.user).delete()
            models.transactions.objects.filter(user=instance.user).delete()
            log_notification(request, "Invoice expired", "Your invoice expired .")

        except:
            pass
