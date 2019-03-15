#!/usr/bin/python3

import os
import datetime
import telegram
# import logging
import time
from watcher import Watcher
from telegram.ext import CommandHandler
from telegram.ext import Updater

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
    print('1 '+time.strftime("%a, %d %b %Y %H:%M:%S"))
def test2():
    print('2 '+time.strftime("%a, %d %b %Y %H:%M:%S"))

w = Watcher()
while 1:
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
    