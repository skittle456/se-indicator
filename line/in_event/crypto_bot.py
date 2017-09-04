import urllib.request
import json
import time
import copy
import datetime
import threading
from .crypto_currency import CryptoCurrency
import line.out_event

send_text = line.out_event.TextMessage()

class CryptoBot:
    def __init__(self, currencies=[]):
        self.bx_url = 'https://bx.in.th/api/'
        self.global_url = 'https://api.coinmarketcap.com/v1/ticker/?convert=THB&limit=20'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        self.cryptocurrencies = self.setup(currencies)
        self.isStart = False
        self.individualAlert = {}
        self.alert = self.setupAlert(currencies)
        self.cmd = "Available Commands:\nBasic Info: !all !btc !eth !das !omg !xrp\nGap Info: #all #btc #eth #das #omg #xrp\nAdd Price Alert (This command is unavailable in group): @[currency] [target] ex. @omg 400.01\nCheck Price Alert: @alert"
        self.updatePrice(False)

    def setup(self, currencies):
        cryptocurrencies = {}
        for currency in currencies:
            cryptocurrencies[currency] = CryptoCurrency(currency)
        return cryptocurrencies

    def setupAlert(self, currencies):
        cryptocurrencies = {}
        for currency in currencies:
            cryptocurrencies[currency] = None
        return cryptocurrencies

    def getBXData(self):
        bx_request = urllib.request.Request(self.bx_url, headers=self.headers)
        bx_response = urllib.request.urlopen(bx_request)
        bx_data = json.loads(bx_response.read().decode(bx_response.info().get_param('charset') or 'utf-8'))
        return bx_data

    def getGlobalData(self):
        global_request = urllib.request.Request(self.global_url, headers=self.headers)
        global_response = urllib.request.urlopen(global_request)
        global_data = json.loads(global_response.read().decode(global_response.info().get_param('charset') or 'utf-8'))
        return global_data

    def getLatestData(self):
        bx_data = self.getBXData()
        global_data = self.getGlobalData()
        return bx_data, global_data

    def updatePrice(self, checkPriceAlert = True):
        try:
            bx_data, global_data = self.getLatestData()
            for key in bx_data:
                data = bx_data[key]
                if data["primary_currency"] == "THB" and data["secondary_currency"] in self.cryptocurrencies:
                    currency = self.cryptocurrencies[data["secondary_currency"]]
                    currency.updateBX(data["last_price"])
            for data in global_data:
                if data["symbol"] == "DASH":
                    data["symbol"] = "DAS"
                if data["symbol"] in self.cryptocurrencies:
                    currency = self.cryptocurrencies[data["symbol"]]
                    old_currency = copy.deepcopy(currency)
                    currency.updateGlobal(data["price_thb"], data["price_usd"], data["percent_change_1h"],
                                          data["percent_change_24h"], data["percent_change_7d"])
                    if checkPriceAlert:
                        self.checkPriceAlert(old_currency, currency)
        except Exception as err:
            self.send(str(err))

    def checkPriceRapidlyChange(self, old_currency, new_currency):
        old_price = float(old_currency.global_price)
        new_price = float(new_currency.global_price)
        output = ""
        if old_price > new_price and new_price / old_price <= 0.9:
            output += "-------------------------\n"
            output += "Price Drop Alert: -" + str(format(old_price / new_price, ".3f")) + "%\n"
            output += "-------------------------\n"
            output += str(new_currency)
            self.send(output)
        elif new_price > old_price and new_price / old_price >= 1.1:
            output += "+++++++++++++++++++++++++\n"
            output += "Price Jump Alert: +" + str(format(new_price / old_price, ".3f")) + "%\n"
            output += "+++++++++++++++++++++++++\n"
            output += str(new_currency)
            self.send(output)

    def checkPriceGap(self):
        result = ""
        try:
            for key in self.cryptocurrencies:
                global_price = float(self.cryptocurrencies[key].global_price)
                bx_price = float(self.cryptocurrencies[key].bx_price)
                gap = max(global_price, bx_price) / min(global_price, bx_price)
                if gap > 0.5:
                    if self.alert[key] % 10 == 0:
                        output = ""
                        output += "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                        output += "Price Gap Alert: " + str(format(gap, ".5f")) + "%\n"
                        output += "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                        output += str(self.cryptocurrencies[key])
                        result +=output
                    self.alert[key] += 1
                else:
                    self.alert[key] = 0
            if result:
                self.send(result)
        except Exception as err:
            self.send(str(err))

    def displayAlert(self, receiver):
        output = "Alert List"
        try:
            for currency in self.individualAlert[receiver]:
                output += "\n" + currency + " at " + self.individualAlert[receiver][currency]
        except KeyError:
            self.individualAlert[receiver] = self.alert
        self.send(output, receiver)

    def checkPriceGap(self, key):
        global_price = float(self.cryptocurrencies[key].global_price)
        bx_price = float(self.cryptocurrencies[key].bx_price)
        gap = (1 - max(global_price, bx_price) / min(global_price, bx_price)) * 100
        output = ""
        output += "Price Gap: " + str(format(gap, ".5f")) + "%\n"
        output += str(self.cryptocurrencies[key])
        return output

    def priceAlert(self, currency, target, receiver):
        try:
            self.individualAlert[receiver][currency] = target
        except KeyError:
            self.individualAlert[receiver] = self.alert
            self.individualAlert[receiver][currency] = target
        output = currency + " price alert added at " + str(target)
        self.send(output, receiver)

    def checkPriceAlert(self, old_currency, new_currency):
        for user in self.individualAlert:
            for currency in self.individualAlert[user]:
                if self.individualAlert[user][currency] is not None:
                    old_price = float(old_currency.global_price)
                    new_price = float(new_currency.global_price)
                    if max(old_price, new_price) >= self.individualAlert[user][currency] >= min(old_price, new_price):
                        output = "Price Alert: " + currency + " reached " + str(new_price)
                        self.send(output, user)
                        self.individualAlert[user][currency] = None

    def displayPrice(self, receiver):
        for currency in self.cryptocurrencies:
            self.send(str(self.cryptocurrencies[currency]), receiver)

    def displayAllGapPrice(self, receiver):
        for currency in self.cryptocurrencies:
            self.send(self.checkPriceGap(currency), receiver)

    def displayGapPrice(self, currency, receiver):
        self.send(self.checkPriceGap(currency), receiver)

    def hrAlarm(self):
        now = datetime.datetime.now()
        if now.minute == 0:
            self.displayPrice()

    def timer(self):
        while True:
            self.updatePrice()
            time.sleep(60)

    def command(self, text, receiver, isGroup):
        if not self.isStart and text != "!start":
            self.send("Timer is currently disable, please contact admin to manually enable it", receiver)
        if len(text) == 0:
            return
        if text[0] == "!":
            text = text.replace("!", "").upper()
            if text == "START" and not self.isStart and receiver == "U240d56479788aaaa4749161398058a17":
                self.isStart = True
                timer = threading.Thread(target=self.timer)
                timer.start()
                self.send("Timer is now online")
            elif text == "CMD":
                self.updatePrice()
                self.send(self.cmd, receiver)
            elif text == "ALL":
                self.updatePrice()
                self.displayPrice(receiver)
            elif text in self.cryptocurrencies:
                self.updatePrice()
                self.send(str(self.cryptocurrencies[text]), receiver)
        elif text[0] == "#":
            text = text.replace("#", "").upper()
            if text == "ALL":
                self.updatePrice()
                self.displayAllGapPrice(receiver)
            elif text in self.cryptocurrencies:
                self.updatePrice()
                self.displayGapPrice(text, receiver)
        elif text[0] == "@":
            text = text.replace("@", "").upper()
            if text == "ALERT":
                self.displayAlert(receiver)
            if isGroup:
                self.send("This command is unavailable in group", receiver)
            else:
                textlist = text.split()
                if len(textlist) == 2:
                    try:
                        target = float(textlist[1])
                    except ValueError:
                        return
                    if textlist[0] in self.cryptocurrencies:
                        self.priceAlert(textlist[0], target, receiver)

    def send(self, output, receiver):
        #C86005bee32f9d3c4bf55fc49b6b2b1fd
        #R5a8df70a7425c3c8b60204f8176dcbcc
        #U240d56479788aaaa4749161398058a17
        send_text.push(receiver, output)