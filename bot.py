#!/usr/bin/python3

import os
import datetime
import telegram
import logging
import urllib.request
import json
import schedule
import time

from telegram.ext import CommandHandler
from telegram.ext import Updater

class MetroTimer:

    started = False
    executed = 0

    # timeout em minutos
    def __init__(self, timeoutMin=30):
        self.executed = 0
        self.timeoutMin = timeoutMin

    def job(self):
        print('test...',self.executed,' ',datetime.datetime.now())


    def start(self):
        self.started = True
        schedule.every(self.timeoutMin).minute.do(self.job)
        while self.started:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        self.started = False

url = ''
apikey = ''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=apikey)
dispatcher = updater.dispatcher

def eco(bot, update):
  print(datetime.datetime.now(), 'eco')
  bot.send_message(chat_id=update.message.chat_id, text='eco')


def status(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=getStatus())    

def getStatus():
    res = ''
    try:
        data = urllib.request.urlopen(url).read()
        status = json.loads(data.decode('utf-8'))

        l1 = status['StatusMetro']['ListLineStatus'][0]
        l2 = status['StatusMetro']['ListLineStatus'][1]
        l3 = status['StatusMetro']['ListLineStatus'][2]
        mu = status['StatusMetro']['DateUpdateMetro']
        l4 = status['CurrentLineStatus']['Status']

        res += 'Linha 1 - '+l1['StatusMetro']+' (atualizado: '+mu+')\n'
        res += 'Linha 2 - '+l2['StatusMetro']+' (atualizado: '+mu+')\n'
        res += 'Linha 3 - '+l3['StatusMetro']+' (atualizado: '+mu+')\n'
        res += 'Linha 4 - '+l4+' (atualizado: '+status['CurrentLineStatus']['DateUpdateFormated']+')'

    except:
        res = 'Erro ao executar a consulta.'

    return res

dispatcher.add_handler(CommandHandler('eco', eco))
dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling() 
