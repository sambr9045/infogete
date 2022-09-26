from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dashboard import models as dashboard_model
from . import forms
from django.contrib import messages
import random, os
from django.utils import timezone
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
import online_users.models as onlineuser
from btcwallet.btcWallet import BtcWallet
from dotenv import load_dotenv
from dashboard.views import requestURL


# Create your views here.
load_dotenv()
# cpanel
def cpanel(request):
    btc_wallet = BtcWallet(os.getenv("BTCWALLETNAME"), os.getenv("BTCKEYPHRASE"))

    if request.method == "POST":
        if "send_btc" in request.POST:
            address = request.POST["btcaddress"]
            secret_code = request.POST["secretcode"]
            amount = request.POST["amount"]
            if address == "" or secret_code == "" or amount == "":
                messages.info(request, "invalide entry . FIle out the form ")
                return redirect("cpanel")

            main_code = os.getenv("MAINCODE")
            if main_code == secret_code:
                amount_in_btc = requestURL(
                    f"https://blockchain.info/tobtc?currency=USD&value={amount}"
                )
                m_wallet = btc_wallet.LoadBtcWallet()
                send_wallet = btc_wallet.sendMoneyReceived(
                    m_wallet, address, amount_in_btc
                )
                messages.info(request, send_wallet)
                return redirect("cpanel")
            else:
                messages.info(request, "invalide secret code please try again ")
                return redirect("cpanel")

    user = User.objects.filter(
        username=request.user.username, is_superuser=True, is_staff=True
    )
    if user.exists():
        pass
    else:
        return redirect("login")
    start_date = timezone.now()
    endmonth = timezone.now() + relativedelta(months=-1)

    obj = User.objects
    # total user object
    totalUser = obj.all().count()
    # one month user object
    thisMonthUser = obj.filter(date_joined__range=[endmonth, start_date]).count()
    #  a day user object
    today_user = obj.filter(date_joined__contains=datetime.today().date()).count()

    # online user object
    user_activity_objects = onlineuser.OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    # wallet

    balance = btc_wallet.get_balance()

    user_data = {
        "totaluser": totalUser,
        "onemonth": thisMonthUser,
        "today": today_user,
        "onlineUser": number_of_active_users,
    }
    info = {
        "sub_title": "welcome sir",
        "user_data": user_data,
        "wallet_balance": balance,
    }
    return render(request, "cpanel/cpanel.html", info)


# send available balance
# def sendbalance(request):


def uploadArticle(request):
    # random number generator
    def randomNumber():
        return random.randint(0, 5000)

    if request.POST:
        if "submit_article" in request.POST:
            title = request.POST["article_title"]
            category = request.POST["category"]
            text = request.POST["editordata"]
            ratio = request.POST["ratio"]
            if title == "" or category == "" or text == "" or ratio == "":
                messages.error(request, "Please fill out all input")
                return redirect("uploadarticle")
            save = dashboard_model.article.objects.create(
                article_title=title,
                category=category,
                content=text,
                views=randomNumber(),
                likes=randomNumber(),
                success_ratio=ratio,
            )

            messages.success(request, "article uploaded successfully")
    info = {"sub_title": "Welcome back boss"}
    return render(request, "cpanel/uploadarticle.html", info)
