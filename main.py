from flask import Flask, request
import telegram # pip install python-telegram-bot
import os
from dotenv import load_dotenv

load_dotenv()

# todo: get telegram to actually SEND THE MESSAGE OVER PLS

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

# --- Message Handlers ---

def handle_start(update):
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="Welcome! I'm your bot.")
    print('sent message')

def handle_help(update):
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="Send any message and I’ll echo it.")
    print('sent message')

def handle_text(update):
    chat_id = update.message.chat.id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text=f"You said: {text}")
    print('sent message')

# --- Dispatcher via Webhook ---

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = telegram.Update.de_json(data, bot)
    print("Received update:", update)

    if update.message:
        text = update.message.text or ""
        if text.startswith('/start'):
            handle_start(update)
        elif text.startswith('/help'):
            handle_help(update)
        else:
            handle_text(update)
    return "ok"