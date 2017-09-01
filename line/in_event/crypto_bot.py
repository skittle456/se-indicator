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
        self.alert = self.setupAlert(currencies)
        self.command = "!btc !eth !das !omg !xrp"
        print('cryptobot been init')
        #timer = threading.Thread(target=self.timer)
        #timer.start()
        self.timer()

    def setup(self, currencies):
        cryptocurrencies = {}
        for currency in currencies:
            cryptocurrencies[currency] = CryptoCurrency(currency)
        return cryptocurrencies

    def setupAlert(self, currencies):
        cryptocurrencies = {}
        for currency in currencies:
            cryptocurrencies[currency] = 0
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

    def updatePrice(self, checkRapidlyPriceChange=True):
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
                    if checkRapidlyPriceChange:
                        self.checkPriceRapidlyChange(old_currency, currency)
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
        print('checkGap called!!')
        used = []
        try:
            for key in self.cryptocurrencies:
                global_price = float(self.cryptocurrencies[key].global_price)
                bx_price = float(self.cryptocurrencies[key].bx_price)
                gap = max(global_price, bx_price) / min(global_price, bx_price)
                if key not in used:
                    if gap > 0.5:
                        if self.alert[key] % 10 == 0:
                            output = ""
                            output += "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                            output += "Price Gap Alert: " + str(format(gap, ".5f")) + "%\n"
                            output += "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                            output += str(self.cryptocurrencies[key])
                            self.send(output)
                        self.alert[key] += 1
                    else:
                        self.alert[key] = 0
                    used.append(key)
        except Exception as err:
            self.send(str(err))

    def displayPrice(self):
        output = ""
        for currency in self.cryptocurrencies:
            output += str(self.cryptocurrencies[currency]) + "\n"
        self.send(output)

    def hrAlarm(self):
        now = datetime.datetime.now()
        if now.minute == 0:
            self.displayPrice()

    def timer(self):
        print('timer called')
        self.updatePrice(False)
        while True:
            print('while true called')
            self.updatePrice()
            self.hrAlarm()
            self.checkPriceGap()
            time.sleep(60)

    def command(self, text):
        if len(text) == 0:
            return
        if text[1] != "!":
            return
        text = text.replace("!", "").upper()
        if text == "command":
            self.send(output=self.command)
        elif text in self.cryptocurrencies:
            self.send(output=str(self.cryptocurrencies[text]))

    def send(self, output, receiver = 'C86005bee32f9d3c4bf55fc49b6b2b1fd'):
        send_text.push(receiver, 'kwai pun'+output)
