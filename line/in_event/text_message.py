import line.out_event
from .crypto_bot import CryptoBot
from .crypto_currency import CryptoCurrency

send_text = line.out_event.TextMessage()
currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
cryptoBot = line.in_event.CryptoBot(currencies)
print('cryptobot created')
class TextMessage(object):
    def __init__(self):
        # self.currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
        # self.cryptoBot = CryptoBot(self.currencies)
        print('textMessage been init!!!')
    def core(self, event):
        #nput = event.message.text
        #self.cryptoBot.command(input)
        pass