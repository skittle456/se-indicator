from flask_restplus import Api

from .line_webhook import api as line_webhook
from line.in_event import CryptoBot
api = Api(
    title='Apis',
    version='1.0',
    description='Apis',
    # All API metadatas
)
api.add_namespace(line_webhook)
#currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
#cryptoBot = CryptoBot(currencies)
print('cryptoBot created ja')
