from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
import pprint

from django.apps import apps
from dotenv import load_dotenv
import os, json
import time
from decimal import Decimal
import threading, json
from datetime import datetime
from dateutil.relativedelta import *
from datetime import timedelta
from django.utils import timezone
import requests


load_dotenv()


class BtcWallet:
    def __init__(self, walletname=None, walletkey=None) -> None:
        self.walletname = walletname
        self.walletkey = walletkey

    def Addressbalance(self):
        pass

    def GetModel(self, appname="dashboard", dbname="transactions"):
        return apps.get_model(appname, dbname)

    def FindAddress(self, address, models):
        data = models.objects.filter(btc_address=address)
        return data.exists()

    def GenerateAddress(self):

        address, numbers = "", 1
        w = self.LoadBtcWallet()
        address = w.get_key().address
        data = self.FindAddress(address, self.GetModel())

        while data:
            address = w.get_key(change=numbers).address
            data = self.FindAddress(address, self.GetModel())
            if data:
                numbers += 1
            else:
                return address
        return address

    def CreateWallet(self):
        w = Wallet.create(
            "InfogetobtcWallet_unique", keys=self.CreateKeyPrase(), network="bitcoin"
        )
        print(w)
        return w

    def CreateKeyPrase(self):

        keyprhase = Mnemonic().generate()
        print(keyprhase)
        return keyprhase

    def LoadBtcWallet(self):
        wallet = Wallet(self.walletname, main_key_object=self.walletkey)
        return wallet

    def get_balance(self):
        w = self.LoadBtcWallet()
        # w.scan()
        balance_satoshi = w.balance()
        balance_btc = int(balance_satoshi) / 100000000
        balance_in_usd = self.BtcToUsd(float(balance_btc))
        return [balance_btc, balance_in_usd]

    def monitor(self, instance):
        wallet = self.LoadBtcWallet()
        while True:
            wallet.scan()
            key = wallet.key(instance.btc_address)
            balance = key.balance()
            if int(balance) > 0:

                def infuct(balance):
                    pass

                btc = Decimal(balance / 100000000)
                btc = round(float(btc), 9)
                data = self.essentials(instance.btc_address, wallet)
                price = self.BtcToUsd(btc)
                data.append(price)

                # check if user paid the total amount of money
                suscription = self.GetModel("dashboard", "suscriptions").objects.filter(
                    user=instance.user
                )

                suscription_total = suscription.first().amountTotal
                if price < self.percentage(95, suscription_total):

                    print(f"{price} is less {suscription_total}")
                    print(self.percentage(95, suscription_total))

                # check for confirmation s
                if int(data[2]) < 2:

                    # continue and update transactions model is confirmation < 2
                    save = self.GetModel()
                    save.objects.filter(
                        transactions_id=instance.transactions_id
                    ).update(
                        amount=price,
                        transaction_hash=data[0],
                        confirmation=int(data[2]),
                        updated_at=timezone.now(),
                    )

                elif int(data[2]) >= 2 or data.status == "confirmed":

                    print(data)
                    return [instance.transaction_type, data]
            else:
                if self.MinuteAgo(instance.created_at, 30) <= 0:
                    balance = 0
                    print("threadind breaks")
                    return [0, [0, 0, 0, balance]]
                print("thread running")

            time.sleep(30)

    def percentage(self, percent, whole):
        return (percent * whole) / 100.0

    def BtcToUsd(self, amount_in_btc):
        url = "https://api.pro.coinbase.com/products/BTC-USD/ticker"
        data = requests.get(url)
        data = data.json()
        price = float(data["price"]) * float(amount_in_btc)
        return round(price, 2)

    def essentials(self, address, wallet):
        try:
            transaction_hash = wallet.transaction_last(address)
            transaction = wallet.transaction(transaction_hash)
            status = transaction.status
            confirmation = transaction.confirmations
            return [transaction_hash, status, confirmation]
        except Exception as e:
            print(e)
            return e

    def MinuteAgo(self, updated_time, minutes):
        # timestamp now + 40 minutes
        timeSus = datetime.now(timezone.utc) + timedelta(minutes=-minutes)
        # convert time into array
        remaining_time = str(updated_time - timeSus).split(":")
        if int(remaining_time[1]) < int(minutes):
            return int(remaining_time[1])

    def sendMoneyReceived(self, wallet, address, balance):
        try:
            amount = str(balance) + " BTC"
            wallet.scan()
            s = wallet.sweep(address, offline=False)
            information = s.info()
            return information

        except Exception as e:
            print(e)
            return e


if __name__ == "__main__":
    w = BtcWallet(os.getenv("BTCWALLETNAME"), os.getenv("BTCKEYPHRASE"))
    s = w.LoadBtcWallet()
    while True:
        s.scan(account_id=0)
        t = s.sweep("bc1qvhy93t7sryzjlne2f0jeqrc490vmuper76jc88", offline=False)
        print(t)
        print(t.info())

        time.sleep(60)
