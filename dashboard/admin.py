from django.contrib import admin
from . import models

# Register your models here.
class TicketRegister(admin.ModelAdmin):
    model: models.ticket
    list_display = (
        "user",
        "subject",
        "message",
        "admin_response",
        "status",
        "updated_at",
        "create_at",
    )


admin.site.register(models.ticket, TicketRegister)

# register admin suscription model


class SuscriptionPlan(admin.ModelAdmin):
    model: models.suscriptions
    list_display = (
        "user",
        "plan",
        "periode",
        "amountTotal",
        "expired_on",
        "reactivate",
        "paid",
        "plan_active",
        "updated_at",
        "created_at",
    )


admin.site.register(models.suscriptions, SuscriptionPlan)


# register transactions model


class TransactionM(admin.ModelAdmin):
    model: models.transactions
    list_display = (
        "user",
        "btc_address",
        "amount",
        "transactions_id",
        "transaction_hash",
        "confirmation",
        "updated_at",
        "created_at",
    )


admin.site.register(models.transactions, TransactionM)


class notificationS(admin.ModelAdmin):
    model: models.notifications
    list_display = (
        "user",
        "notifications_id",
        "title",
        "message",
        "read",
        "created_at",
    )


admin.site.register(models.notifications, notificationS)


class articleviws(admin.ModelAdmin):
    model: models.articleView
    list_display = ("user", "article", "view", "like", "create_at")


admin.site.register(models.articleView, articleviws)


# register categorie models


class categories(admin.ModelAdmin):
    model: models.category
    list_display = ("category",)


admin.site.register(models.category, categories)

# register interest model
class Useinterest(admin.ModelAdmin):
    model: models.interest
    list_display = ("list_of_interest", "created_at")


admin.site.register(models.interest, Useinterest)


# regirster plan upgrade model


class planUpgrade(admin.ModelAdmin):
    model = models.upgradePlan
    list_display = ("id", "user", "active", "created_at")


admin.site.register(models.upgradePlan, planUpgrade)


# register plan save_article models


class save_articles(admin.ModelAdmin):
    model: models.save_article
    list_display = ("user", "articleid", "created_at")


admin.site.register(models.save_article, save_articles)
