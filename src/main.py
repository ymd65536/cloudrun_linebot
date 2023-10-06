import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config

import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.language_models import ChatModel
from vertexai.language_models import InputOutputTextPair

app = Flask(__name__)
line_bot_api = LineBotApi(config.token)
handler = WebhookHandler(config.secret)

parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}


@app.route("/")
def hello_world():

    vertexai.init(location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        "Who are you?",
        **parameters
    )

    return f"{response.text}!"


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    event_type = event.type
    message_type = event.message.type
    vertexai.init(location="us-central1")

    if event_type == 'message':
        if message_type == 'text':
            chat_model = ChatModel.from_pretrained("chat-bison@001")

            chat = chat_model.start_chat(
                context="あなたは文章をきれいにまとめることができるアシスタントです。入力された要約してください。",
                examples=[
                    InputOutputTextPair(
                        input_text="Your name",
                        output_text="Kento.Yamada@ymd65536",
                    )
                ],
                temperature=0.3,
            )

            response = chat.send_message(event.message.text)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response.text)
            )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
