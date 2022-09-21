from email.policy import default
from pydoc import plain
from pyexpat import model
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
import uuid

# Create your models here.
class ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)
    subject = models.CharField(max_length=200, null=False)
    message = models.TextField(null=False)
    admin_response = models.TextField(null=True)
    status = models.CharField(default="pending", null=False, max_length=200)
    updated_at = models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(default=timezone.now)


class suscriptions(models.Model):
    class PlanChoice(models.TextChoices):
        basic = "basic", "basic"
        standart = "standart", "standart"
        premium = "premium", "premium"
        default = "None", "None"

    user = models.ForeignKey(User, default=None, null=False, on_delete=models.CASCADE)
    plan = models.CharField(
        max_length=20, choices=PlanChoice.choices, default=PlanChoice.default
    )
    periode = models.IntegerField(default=None)
    amountTotal = models.FloatField(default=None)
    expired_on = models.DateTimeField(default=None)
    reactivate = models.IntegerField(default=0, null=False)
    paid = models.BooleanField(default=False)
    plan_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)


class transactions(models.Model):
    user = models.ForeignKey(User, default=None, null=False, on_delete=models.CASCADE)
    suscriptions = models.ManyToManyField(suscriptions)
    btc_address = models.CharField(max_length=200, null=False, default=None)
    amount = models.FloatField(default=None)
    transactions_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    transaction_type = models.CharField(max_length=200, default="newplan")
    transaction_hash = models.TextField(default=None, null=True)
    confirmation = models.IntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)


class notifications(models.Model):
    user = models.ForeignKey(User, default=None, null=False, on_delete=models.CASCADE)
    notifications_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=200, default=None)
    message = models.TextField(default=False)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class article(models.Model):
    article_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_title = models.CharField(max_length=200, default=None)
    category = models.CharField(max_length=200, default=None, null=False)
    content = HTMLField(default=None)
    views = models.IntegerField(default=None)
    likes = models.IntegerField(default=None)
    success_ratio = models.CharField(max_length=5, default=None)
    created_at = models.DateTimeField(default=timezone.now)


class articleView(models.Model):
    user = models.ForeignKey(User, default=None, null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(
        article, default=None, null=False, on_delete=models.CASCADE
    )
    view = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=timezone.now)


class upgradePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    suscriptions = models.ManyToManyField(suscriptions, default=None)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class category(models.Model):
    category = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(default=timezone.now)


class interest(models.Model):
    user = models.ForeignKey(User, default=None, null=False, on_delete=models.CASCADE)
    list_of_interest = models.TextField(default=None)
    created_at = models.DateTimeField(default=timezone.now)


class partial_payment(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)


class save_article(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    articleid = models.UUIDField(default=None)
    saved_article = models.ManyToManyField(article, default=None)
    created_at = models.DateTimeField(default=timezone.now)
