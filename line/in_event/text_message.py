import line.out_event
from .crypto_bot import CryptoBot
send_text = line.out_event.TextMessage()

currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
instance = None

class TextMessage(object):
    def __init__(self):
        global instance
        if instance is None:
            self.cryptoBot = CryptoBot(currencies)
            instance = self.cryptoBot
        else:
            self.cryptoBot = instance

    def core(self, event):
        if event.source.type == "group":
            self.cryptoBot.command(event.message.text, event.source.group_id, True)
        elif event.source.type == "user":
            self.cryptoBot.command(event.message.text, event.source.user_id, False)