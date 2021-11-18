import os

from decouple import config
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MemberJoinedEvent, MessageEvent, TextMessage,
                            TextSendMessage)

app = Flask(__name__)

# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)

# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(404)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    msg = event.message.text
    if msg[0:2] == '/r' and msg[2] == ' ':
        name = msg.split()[2]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='proceed to roasting ' + name+', please wait...')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='your message: ' + msg)
        )


@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    member = event.joined.members[0]
    memberId = member.userId
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='There is a user joined with id: ' + memberId +
                        ', Your event type is : ' + event.type)
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
