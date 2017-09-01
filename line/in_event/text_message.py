import line.out_event
from line.in_event import CryptoBot

send_text = line.out_event.TextMessage()

class TextMessage(object):
    def __init__(self):
        self.currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
        self.cryptoBot = CryptoBot(self.currencies)

    def core(self, event):
        input = event.message.text.lower()
        self.cryptoBot.command(input)
