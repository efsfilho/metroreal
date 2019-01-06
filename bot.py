#!/usr/bin/python3

import telegram
import logging


from telegram.ext import CommandHandler
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



updater = Updater(token='apik')
dispatcher = updater.dispatcher

def eco(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='eco')

dispatcher.add_handler(CommandHandler('eco', eco))

updater.start_polling()