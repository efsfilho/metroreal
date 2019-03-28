#!/usr/bin/python3

import os
import datetime
import telegram
import time
import logging
from watcher import Watcher
from telegram.ext import CommandHandler, Updater

logger = logging.getLogger('telegram')
logger.setLevel(logging.INFO)

apikey = os.environ['b1']

updater = Updater(token=apikey)
dispatcher = updater.dispatcher

# w = Watcher()
w = Watcher(interval=5, startTime='17:31', stopTime='17:50', rushInterval=2,
            rushStartTime='17:45', rushStopTime='17:50')
# w.start()

from functools import wraps
LIST_OF_ADMINS = [] # usuario permitido

# Filtro de usuário
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        # user_id = context.message.chat.id
        user = context.message.chat
        if user.id not in LIST_OF_ADMINS:
            logging.info(f'Unauthorized access denied for {user}.')
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def status(bot, update):
    # TODO try
    status = w.getStatus()
    bot.send_message(chat_id=update.message.chat_id, text=status)

@restricted
def eco(bot, update):
    logging.debug('eco debug');
    bot.send_message(chat_id=update.message.chat_id, text='ecossss')

def ini(bot, update):
    logging.info('ininin');

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling() 
print('key '+apikey)

# w = Watcher(interval=4, startTime='17:31', stopTime='17:30', rushInterval=2,
#             rushStartTime='16:55', rushStopTime='16:57')
# # w = Watcher()
# loop = True
# while loop:
#     command = input()
#     if command == 'start':
#         w.start()
#     if command == 'status':
#         print(w.is_alive())
#     if command == 'stop':
#         w.stop()
#     if command == 'c1':
#         w.clear('updateJob')
#     if command == 'exit':
#         if w.is_alive():
#             w.stop()
#         loop = False



