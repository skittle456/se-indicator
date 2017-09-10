import line.out_event
from .crypto_bot import CryptoBot
send_text = line.out_event.TextMessage()

currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]

class TextMessage(object):
    def __init__(self):
        self.cryptoBot = CryptoBot(currencies)
        print('TextMessage Init')

    def core(self, event):
        if event.source.type == "group":
            self.cryptoBot.command(event.message.text, event.source.group_id, True)
        elif event.source.type == "user":
            self.cryptoBot.command(event.message.text, event.source.user_id, False)