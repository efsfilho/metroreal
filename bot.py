#!/usr/bin/python3

import os
import datetime
import telegram
import time
from watcher import Watcher
from telegram.ext import CommandHandler, Updater

# TODO logging
import logging
log_format = '%(asctime)s - %(name)s - [%(levelname)-7s] - %(message)s'
logging.basicConfig(filename='log.log', filemode='a+', level=logging.INFO, format=log_format)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(consoleHandler)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

apikey = os.environ['b1']

updater = Updater(token=apikey)
dispatcher = updater.dispatcher

w = Watcher()

def start(bot, update):
    w.start()
    bot.send_message(chat_id=update.message.chat_id, text='ecossss')

def status(bot, update):
    status = w.is_alive()
    status = 's'
    bot.send_message(chat_id=update.message.chat_id, text=status)

def stop(bot, update):
    if w.is_alive():
        w.stop()
    status(bot, update)

def eco(bot, update):
  logging.debug('eco debug');
  bot.send_message(chat_id=update.message.chat_id, text='ecossss')

def ini(bot, update):
  logging.info('ininin');

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(CommandHandler('stop', stop))

updater.start_polling() 
print('key '+apikey)


# w = Watcher(interval=4, startTime='17:31', stopTime='17:30', rushInterval=2,
#             rushStartTime='16:55', rushStopTime='16:57')
# w = Watcher()
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
    # if command == 'exit':
    #     if w.is_alive():
    #         w.stop()
    #     loop = False








