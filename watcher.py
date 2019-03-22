import time
import json
import schedule
import urllib.request
import datetime
from threading import Thread

import logging
log_format = '%(asctime)s - [%(name)-10s] - [%(levelname)-7s] - %(message)s'
logging.basicConfig(filename='log.log', filemode='a+', level=logging.DEBUG, format=log_format)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(consoleHandler)

def dateformat(dt):
    return time.strftime("%a, %d %b %Y %H:%M:%S", dt)

def writeJson(data):
    with open('data.json', 'a', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write('\n')

class Watcher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._running = False
        self._dataStatus = []

        self._mainTaskTag = 'updateTask'
        self._mainTaskInterval = 2 # minutos

        self._rushTaskTag = 'rushTask'
        self._rushTaskInterval = 1 # minutos

    def run(self):
        if self._running:
            return
        self._running = True
        logging.info('Watcher started!')
        
        self._setSchedule()

        while self._running:
            schedule.run_pending()
            time.sleep(1)

        logging.info('Watcher finished!')

    def _setSchedule(self):
        """
        1 - inicia o watcher normal: _startWatcher
        2 - para o watcher normal e inicia o watcher rush: _startRushWatcher
        3 - para o watcher rush e inicia o watcher normal: _stopRushWatcher 
        4 - para o watcher normal: _stopWatcher
        """

        # 1  normal  2  rush  3  normal  4
        # [----------[========]----------]
        schedule.every().day.at('04:00').do(self._startWatcher)     # 1
        schedule.every().day.at('22:00').do(self._stopWatcher)      # 4
        schedule.every().day.at('16:50').do(self._startRushWatcher) # 2
        schedule.every().day.at('19:00').do(self._stopRushWatcher)  # 3

    def _startWatcher(self):
        jobTag = self._mainTaskTag
        interval = self._mainTaskInterval
        schedule.every(interval).minutes.tag(jobTag).do(self._updateDataStatus)

    def _stopWatcher(self):
        schedule.clear(self._mainTaskTag)

    def _startRushWatcher(self):
        jobTag = self._rushTaskTag
        interval = self._rushTaskInterval
        self._stopWatcher()
        schedule.every(interval).minutes.tag(jobTag).do(self._updateDataStatus)

    def _stopRushWatcher(self):
        schedule.clear(self._rushTaskTag)
        self._startWatcher()

    def clear(self, tag=None):
        schedule.clear(tag)

    def _updateDataStatus(self):
        data = None
        try:
            req = urllib.request.urlopen('https://www.diretodostrens.com.br/api/status')
            data = json.loads(req.read().decode('utf-8'))
        except urllib.error.HTTPError as err:
            logging.error('watcher > _updateDataStatus > HTTPError code: '+str(err.code))
        except urllib.error.URLError as err:    
            logging.error('watcher > _updateDataStatus > Request error: '+str(err.reason))
        except json.decoder.JSONDecodeError as err:
            logging.error('watcher > _updateDataStatus > JSON decode error: '+ str(err))
        finally:
            if data != None:
                self._dataStatus = data
                for linha in self._dataStatus:
                    if ('situacao' in linha) and (linha['situacao'] != 'Operação Normal'):
                        logging.debug(linha)

    def stop(self):
        self._running = False