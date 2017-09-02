import line.out_event
from .crypto_bot import CryptoBot
send_text = line.out_event.TextMessage()

class TextMessage(object):
    def __init__(self):
        self.currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
        self.cryptoBot = CryptoBot(self.currencies)

    def core(self, event):
        print(event.source.type)
        if event.source.type == 'group':
            print(type(event.source.group_id))
            self.cryptoBot.command(event.message.text, event.source.group_id)
        else:
            print(type(event.source.user_id))
            self.cryptoBot.command(event.message.text, event.source.user_id)