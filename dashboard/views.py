from asyncore import read
from calendar import month
from distutils.log import info
from email import message
from http.client import HTTPResponse
from re import search
import re
from time import time
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages

from . import forms, models
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import logout as LogoutV
from btcwallet.btcWallet import BtcWallet
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import *
from requests import get
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from landingpage.views import MinuteAgo
from django.core.paginator import Paginator
from django.contrib.auth.models import User


load_dotenv()

# bad code practive from function dashboard() to homeCategorie
# duplication should probably create a fuction
# but tight
@login_required(login_url="/login")
def dashboard(request):
    article = models.article.objects.all().order_by("-created_at")[0:10]
    category = models.category.objects.all()
    # check if user suscription expired
    suscriptions = models.suscriptions.objects.filter(user=request.user)
    if suscriptions.exists():
        if suscriptions.first().expired_on < timezone.now():
            # update user plan
            suscriptions.update(paid=False, plan_active=False)

    if "category" in request.GET:
        categori = str(request.GET["category"])
        article = models.article.objects.filter(category=categori).order_by(
            "-created_at"
        )[0:10]
    if "searche" in request.GET:
        search = str(request.GET["searche"])
        article = models.article.objects.filter(article_title__contains=search)

    paginator = Paginator(article, 10)
    page = request.GET.get("page")
    if page == None:
        pages = "0"
    else:
        pages = int(page)
    article = paginator.get_page(page)

    info = {
        "sub_title": "Your tutorials for this week",
        "article": article,
        "category": category,
        "pageNumber": pages,
    }

    return render(request, "dashboard/home.html", info)


# @login_required(login_url="/login")
# def homeCatedorie(request, categorie):
#     article = models.article.objects.filter(category=categorie).order_by("-created_at")[
#         0:10
#     ]
#     category = models.category.objects.all()
#     info = {
#         "sub_title": "Your tutorials for this week",
#         "article": article,
#         "category": category,
#     }
#     return render(request, "dashboard/homecategorie.html", info)


@csrf_exempt
@login_required(login_url="/login")
def viewarticle(request, uuid, title):
    if request.POST:
        if "likearticle" in request.POST:
            article_id = request.POST["likearticle"]

            if models.articleView.objects.filter(article_id=str(article_id)).exists():
                return HttpResponse("none")
            else:
                # update article like
                models.article.objects.filter(article_id=str(article_id)).update(
                    likes=F("likes") + 1
                )
                # update view article
                models.articleView.objects.filter(article_id=str(article_id)).update(
                    like=True
                )

                return HttpResponse("200")
    suscriptions = models.suscriptions.objects.filter(user=request.user)

    if not suscriptions:
        messages.info(
            request,
            "You need to suscribe to a plan to continue reading",
        )
        return redirect("suscriptions")
    elif suscriptions.exists() and suscriptions.first().plan_active == False:
        messages.info(request, "Please complete your suscription payment ")
        return redirect("suscriptions")

    data = models.article.objects.filter(article_id=uuid).first()

    viewarticle = models.articleView.objects.filter(user=request.user, article=data)

    if viewarticle.exists() and viewarticle.first().view == False:
        models.article.objects.filter(article_id=uuid).update(views=F("view") + 1)
        viewarticle.update(views=True)
    elif not viewarticle:
        models.article.objects.filter(article_id=uuid).update(views=F("views") + 1)
        models.articleView.objects.create(
            user=request.user,
            article=data,
            view=True,
        )

    data = models.article.objects.filter(article_id=uuid).first()

    info = {
        "sub_title": data.article_title,
        "data": data,
        "viewarticle": viewarticle.first(),
    }
    return render(request, "dashboard/viewarticle.html", info)


@login_required(login_url="/login")
def tickets(request):
    form = forms.TicketForm()
    if request.method == "POST":
        if "delete_ticket" in request.POST:
            TicketId = request.POST["tiketPk"]
            models.ticket.objects.filter(pk=TicketId, user=request.user).delete()
            messages.success(request, "Ticket deleted succesfully")
            return redirect("tickets")
        if "openTicket" in request.POST:

            form = forms.TicketForm(request.POST)
            subject = request.POST["subject"]
            message = request.POST["message"]

            if subject == "" or message == "":
                messages.error(
                    request, "invalide Input . Please field out all the input"
                )
                return redirect("tickets")

            ticketSave = models.ticket.objects.create(
                user=request.user, subject=subject, message=message, admin_response=None
            )

            messages.success(request, "Ticket submited succesfully")
            return redirect("viewTicket", ticketSave.pk)

    tickets = models.ticket.objects
    all_ticket = tickets.filter(user=request.user).count
    closed_ticket = tickets.filter(status="close", user=request.user).count
    pending_ticket = tickets.filter(status="pending", user=request.user).count
    ticket_info = {
        "all_ticket": all_ticket,
        "closed_ticket": closed_ticket,
        "pending_ticket": pending_ticket,
    }

    info = {
        "sub_title": "You need help ? open a ticket . We will get back to you as soon as possible",
        "form": form,
        "tickets": ticket_info,
    }
    return render(request, "dashboard/tickets.html", info)


@login_required(login_url="/login")
def viewTicket(request, id):
    data = models.ticket.objects.filter(user=request.user, pk=id).first()
    return render(request, "dashboard/ticketdetails.html", {"data": data})


@login_required(login_url="/login")
def contactUs(request):
    return render(request, "dashboard/contactUs.html")


@login_required(login_url="/login")
def ticketList(request, status):
    data = ""
    if status == "all":
        data = models.ticket.objects.filter(user=request.user).order_by("-create_at")
    else:
        data = models.ticket.objects.filter(
            status=str(status), user=request.user
        ).order_by("-create_at")
    ticket = {"tickets_list": data}
    return render(request, "dashboard/list.html", ticket)


@csrf_exempt
def n_notification(request):
    if request.method == "POST":
        notification = models.notifications.objects.filter(
            user=request.user, read=False
        )
        if notification.exists():
            notification.update(read=True)

        return HttpResponse("done")


@login_required(login_url="/login")
def suscriptions(request):

    if request.method == "POST":
        if "cancel_transactions_plan" in request.POST:
            thuuid = request.POST.get("transaction_id")
            models.transactions.objects.filter(
                transactions_id=thuuid, user=request.user
            ).delete()
            plan = models.suscriptions.objects.filter(user=request.user)
            plans = plan.first().plan
            plan.delete()
            messages.success(
                request,
                "Suscriptions plan canceled successfully. Feel free to explore different plans",
            )
            log_notification(
                request,
                "Suscription",
                f"your {plans} suscription  plan has been canceled.",
            )
            return redirect("suscriptions")
    transactions = models.transactions.objects.filter(user=request.user).first()
    plan = models.suscriptions.objects.filter(user=request.user).first()
    url = "dashboard/suscriptions.html"

    if plan is not None:
        plantext = PlanText(plan.plan)
        url = "dashboard/planexist.html"

    else:
        plantext = 0

    info = {
        "sub_title": "Your suscriptions plans",
        "plan": plan,
        "transaction": transactions,
        "planText": plantext,
    }

    return render(request, url, info)


def PlanText(plan):
    name = ""
    if plan == "1":
        name = "basic"
    elif plan == "2":
        name = "standart"
    elif plan == "3":
        name = "premieum"
    return name


@login_required(login_url="/login")
def suscribetoplan(request, plan):

    if request.method == "POST":
        if "submit_suscription_plan" in request.POST:
            plan = request.POST["plan"]
            periode = request.POST["periode"]
            periode_total = request.POST["periode_total"]

            suscrip = models.suscriptions.objects.filter(user=request.user, plan=plan)
            payment = models.transactions.objects.filter(user=request.user)
            expired_on = datetime.now() + relativedelta(months=+int(periode))

            if suscrip.exists() and payment.exists():
                return redirect("suscriptions")
            else:
                #
                models.suscriptions.objects.create(
                    user=request.user,
                    plan=plan,
                    periode=periode,
                    amountTotal=periode_total,
                    expired_on=expired_on,
                    reactivate=1,
                )

                wallet = BtcWallet(
                    os.getenv("BTCWALLETNAME"), os.getenv("BTCKEYPHRASE")
                )
                Address = wallet.GenerateAddress()

                instance = models.transactions.objects.create(
                    user=request.user,
                    btc_address=Address,
                    amount=periode_total,
                )
                instance.suscriptions.set(
                    models.suscriptions.objects.filter(user=request.user)
                )
                uuid = instance.transactions_id

                log_notification(
                    request,
                    "suscriptions",
                    f"{plan} plan created for a total of {periode_total} $ . expires on {str(expired_on)[0:10]}",
                )

                return redirect("payment", uuid, plan)

    info = {
        "sub_title": "You’re almost there! Complete your order",
        "periode": planCalculator(plan),
    }

    return render(request, "dashboard/confirmplan.html", info)


def payment(request, uuid, plan):
    payment_data = models.transactions.objects.filter(transactions_id=uuid).first()
    suscription_data = models.suscriptions.objects.filter(user=request.user).first()
    wainting = " wating for payment..."
    if payment_data is None:
        return redirect("suscriptions")
    elif payment_data.transaction_hash is not None and payment_data.confirmation < 2:
        wainting = f" ${payment_data.amount} received {payment_data.confirmation} confirmations"
    elif (
        suscription_data.paid == True
        and suscription_data.plan_active == True
        and payment_data.transaction_type == "newplan"
    ):
        return redirect("suscriptions")

    timeleft = MinuteAgo(payment_data.created_at, 30)

    if timeleft == "0" or timeleft == None:
        delete_sus_tran(request, request.user)

    amount_in_btc = requestURL(
        f"https://blockchain.info/tobtc?currency=USD&value={suscription_data.amountTotal}"
    )
    qrcode_value = f"bitcoin:{payment_data.btc_address}?amount={amount_in_btc}"
    info = {
        "sub_title": "Complete payment",
        "payment_data": payment_data,
        "suscription_data": suscription_data,
        "plan": plan,
        "amount_in_btc": amount_in_btc,
        "remaining_time": timeleft,
        "waiting": wainting,
        "qrcode": qrcode_value,
    }

    return render(request, "dashboard/payment.html", info)


def delete_sus_tran(request, userid):
    models.suscriptions.objects.filter(user=userid).delete()
    models.transactions.objects.filter(user=userid).delete()
    messages.info(request, "Invoice expired !!")


def planCalculator(plan):
    endPrice = 0
    first_period = 1
    second_period = 12
    third_period = 24
    fourth_period = 48
    if plan == "basic":
        endPrice = 10
    elif plan == "standart":
        endPrice = 40
    elif plan == "premium":
        endPrice = 100

    # calculate time
    def p(period):
        return datetime.now() + relativedelta(months=+period)

    periode = {
        "first_period": [
            p(first_period),
            first_period * endPrice,
            first_period,
            endPrice,
            plan,
        ],
        "second_perido": [
            p(second_period),
            second_period * endPrice,
            second_period,
            endPrice,
            plan,
        ],
        "third_period": [
            p(third_period),
            third_period * endPrice,
            third_period,
            endPrice,
            plan,
        ],
        "fourth_period": [
            p(fourth_period),
            fourth_period * endPrice,
            fourth_period,
            endPrice,
            plan,
        ],
    }

    return periode


@login_required(login_url="/login")
def profile(request):
    info = {
        "sub_title": "My profile",
        "user": models.User.objects.filter(username=request.user.username).first(),
        "suscription": models.suscriptions.objects.filter(
            user=request.user, plan_active=True
        ).first(),
    }
    return render(request, "dashboard/profile.html", info)


def requestURL(url):
    result = get(url).content.decode("utf8")
    return result


# upgrade suscriptions plan
@login_required(login_url="/login")
def upgradePlan(request):
    return render(request, "dashboard/upgrade.html")


# renew plan view
@login_required(login_url="/login")
def renew_plan(request):
    status = "active"

    current_suscription = models.suscriptions.objects.filter(user=request.user).first()
    expiration_time_stamp = current_suscription.expired_on
    if current_suscription.expired_on < timezone.now():
        status = "expired"
        expiration_time_stamp = timezone.now()

    expired_date = expiration_time_stamp + relativedelta(
        months=+current_suscription.periode
    )
    if request.POST:
        # get old plan details
        old_plan = models.suscriptions.objects.filter(user=request.user).first()
        # creare new transaction
        # first generate btc addess
        wallet = BtcWallet(os.getenv("BTCWALLETNAME"), os.getenv("BTCKEYPHRASE"))
        Address = wallet.GenerateAddress()

        # save address to database

        instance = models.transactions.objects.create(
            user=request.user,
            btc_address=Address,
            amount=old_plan.periode,
            transaction_type="renew",
        )
        instance.suscriptions.set(models.suscriptions.objects.filter(user=request.user))
        uuid = instance.transactions_id

        log_notification(
            request,
            "suscriptions",
            f"{old_plan.plan} plan created for a total of {old_plan.periode} $ . expires on {str(expired_date)[0:10]}",
        )

        return redirect("payment", uuid, old_plan.plan)

    info = {
        "sub_title": "Renew your plan",
        "current_plan": current_suscription,
        "status": status,
        "expired_date": expired_date,
    }
    return render(request, "dashboard/renew.html", info)


# change user password
def changePassword(request):
    if request.method == "POST":
        old_form_password = str(request.POST["oldpassword"])
        new_password1 = str(request.POST["newpassword1"])
        new_password2 = str(request.POST["newpassword2"])
        current_password = models.User.objects.filter(pk=request.user.pk).first()
        if old_form_password == "" or new_password1 == "" or new_password2 == "":
            messages.info(
                request, "invalide input . Please make sure you fill all the filed"
            )
            return redirect("changepassword")
        if new_password1 != new_password2:
            messages.info(request, "Password do not match ")
            return redirect("changepassword")

        if check_password(old_form_password, current_password.password):
            Newuser = models.User.objects.get(username=request.user.username)
            Newuser.set_password(new_password1)
            Newuser.save()
            messages.success(request, "password changed successfully ")
            return redirect("profile")
        else:
            messages.info(request, "Old password is incorrect")
            return redirect("changepassword")

    return render(request, "dashboard/changePassword.html")


def log_notification(request, title, message):
    models.notifications.objects.create(user=request.user, title=title, message=message)


# read later view
@csrf_exempt
def readLater(request):
    if request.method == "POST":
        article_id = str(request.POST["article_id"])
        obj = models.article.objects.filter(article_id=article_id).first()
        if models.save_article.objects.filter(
            user=request.user, articleid=article_id
        ).exists():
            return HttpResponse(500)
        else:
            if obj:
                save_article = models.save_article.objects.create(
                    user=request.user, articleid=article_id
                )
                save_article.save()
                save_article.saved_article.add(obj)
                return HttpResponse(200)
            else:
                return HttpResponse(404)

    data = models.save_article.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(data, 10)

    page = request.GET.get("page")
    if page == None:
        pages = "0"
    else:
        pages = int(page)
    object = paginator.get_page(page)

    # for i in data.saved_article.all():
    #     print(i.article_id)
    info = {"sub_title": "Saved articles", "data": object, "pageNumber": pages}
    return render(request, "dashboard/readlater.html", info)


def logout(request):
    LogoutV(request)
    return redirect("login")
