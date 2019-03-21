#!/usr/bin/python3

import os
import datetime
import telegram
import time
from watcher import Watcher
from telegram.ext import CommandHandler
from telegram.ext import Updater

# import logging
# log_format = '%(asctime)s - %(name)s - [%(levelname)-7s] - %(message)s'
# logging.basicConfig(filename='log.log', filemode='a+', level=logging.INFO, format=log_format)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logging.Formatter(log_format))
# logging.getLogger().addHandler(consoleHandler)

# logging.debug('BOT debug')
# logging.info('BOT')
# logging.warning('BOT WARNINGSFDSFDF')

# apikey = os.environ['b1']

# updater = Updater(token=apikey)
# dispatcher = updater.dispatcher

# def eco(bot, update):
#   logging.debug('eco debug');
#   watcher.teste()
#   bot.send_message(chat_id=update.message.chat_id, text='eco')

# def ini(bot, update):
#   watcher.start()

# dispatcher.add_handler(CommandHandler('eco', eco))
# dispatcher.add_handler(CommandHandler('ini', ini))
# updater.start_polling() 
# print('key '+apikey)

def test1():
    print('1 '+time.strftime('%a, %d %b %Y %H:%M:%S'))
def test2():
    print('2 '+time.strftime('%a, %d %b %Y %H:%M:%S'))

w = Watcher()
loop = True
while loop:
    command = input()
    if command == 'start':
        w.start()
    if command == 'status':
        print(w.is_alive())
    if command == 'stop':
        w.stop()
    if command == '1':
        w.addJob(test1, '1')
    if command == '2':
        w.addJob(test2, '2')
    if command == 'c1':
        w.clear('1')
    if command == 'c2':
        w.clear('2')
    if command == 'exit':
        loop = False

