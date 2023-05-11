import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# ======python的函數庫==========
import requests
import os
from bs4 import BeautifulSoup
# ======python的函數庫==========
app = Flask(__name__)

""" config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret')) """


static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    """ line_bot_api.reply_message(event.reply_token, TextSendMessage(msg)) """
    if msg.find('查詢未完成工單') != -1:
        url = 'https://sys.leadyoung.com.tw/assets/Home/LINE_BOT_LYE_QueryWOProgress?ID='+msg
        # 發送GET請求
        response = requests.get(url)
        response.close()


if __name__ == "__main__":
    app.run()
