import configparser
import os

from linebot import LineBotApi
from linebot.models import TextSendMessage
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(os.path.dirname(cur_dir), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

line_bot_api = LineBotApi(config['LINE']['ChannelAccessToken'])

print("woo")

class TextMessage(object):
    def __init__(self):
        print("Init")
        return

    def reply(self, reply_token, message):
        packed = self._pack(message)
        line_bot_api.reply_message(reply_token, packed)
        return

    def push(self, user_id, message):
        packed = self._pack(message)
        line_bot_api.push_message(user_id, packed)
        return

    def _pack(self, message):
        packed = TextSendMessage(text=message)
        return packed
