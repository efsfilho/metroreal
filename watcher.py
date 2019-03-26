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
logging.getLogger('schedule').setLevel(logging.WARNING)

def dateformat(dt):
    return time.strftime("%a, %d %b %Y %H:%M:%S", dt)

def writeJson(data):
    with open('data.json', 'a', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write('\n')

class Watcher(Thread):

    def __init__(self, interval=None, startTime=None, stopTime=None, rushInterval=None,
            rushStartTime=None, rushStopTime=None):

        Thread.__init__(self)
        self._running = False
        self._dataStatus = []

        # TODO um valid decente
        if interval == None:
            interval = 30  # minutos

        if startTime == None:
            startTime = '04:00' 

        if stopTime == None:
            stopTime = '22:00'

        if rushInterval == None:
            rushInterval = 15  # minutos

        if rushStartTime == None:
            rushStartTime = '16:50'
            
        if rushStopTime == None:
            rushStopTime = '16:50'

        self._taskTag = 'updateTask'
        self._taskInterval = interval
        self._taskStartTimeStr = startTime
        self._taskStopTimeStr = stopTime

        self._rushTaskTag = 'rushTask'
        self._rushTaskInterval = rushInterval
        self._rushTaskStartTimeStr = rushStartTime
        self._rushTaskStopTimeStr = rushStopTime

        initInfo = '\n*** INIT INFO ***\n'
        initInfo += f'    interval:      {self._taskInterval} (min) \n'
        initInfo += f'    startTime:     {self._taskStartTimeStr} \n'
        initInfo += f'    stopTime:      {self._taskStopTimeStr} \n'
        initInfo += f'    rushInterval:  {self._rushTaskInterval} (min) \n'
        initInfo += f'    rushStartTime: {self._rushTaskStartTimeStr} \n'
        initInfo += f'    rushStopTime:  {self._rushTaskStopTimeStr} \n'
        logging.info(initInfo)

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
        1  normal  2  rush  3  normal  4
        [----------[========]----------]

        1 - inicia o watcher normal: _startWatcher
        2 - para o watcher normal e inicia o watcher rush: _startRushWatcher
        3 - para o watcher rush e inicia o watcher normal: _stopRushWatcher 
        4 - para o watcher normal: _stopWatcher
        """

        schedule.every().day.at(self._taskStartTimeStr).do(self._startWatcher)         # 1
        schedule.every().day.at(self._taskStopTimeStr).do(self._stopWatcher)           # 4
        schedule.every().day.at(self._rushTaskStartTimeStr).do(self._startRushWatcher) # 2
        schedule.every().day.at(self._rushTaskStopTimeStr).do(self._stopRushWatcher)   # 3

        dt = datetime.datetime.utcnow()
        if dt.hour > 4:
            self._startWatcher()

    def _startWatcher(self):
        jobTag = self._taskTag
        interval = self._taskInterval
        # schedule.every(interval).minutes.tag(jobTag).do(self._updateDataStatus)
        schedule.every(interval).seconds.tag(jobTag).do(self._updateDataStatus)
        logging.info(f'_startWatcher: jobTag={jobTag} interval={interval}(min)')

    def _stopWatcher(self):
        jobTag = self._taskTag
        schedule.clear(jobTag)
        logging.info(f'_stopWatcher: jobTag={jobTag}')

    def _startRushWatcher(self):
        jobTag = self._rushTaskTag
        interval = self._rushTaskInterval
        self._stopWatcher()
        # schedule.every(interval).minutes.tag(jobTag).do(self._updateDataStatus)
        schedule.every(interval).seconds.tag(jobTag).do(self._updateDataStatus)
        logging.info(f'_startRushWatcher: jobTag={jobTag} interval={interval}(min)')

    def _stopRushWatcher(self):
        jobTag = self._rushTaskTag
        schedule.clear(jobTag)
        self._startWatcher()
        logging.info(f'_stopRushWatcher: jobTag={jobTag}')
        

    def clear(self, tag=None):
        schedule.clear(tag)

    def _updateDataStatus(self):
        logging.info('_updateDataStatus')
        # data = None
        # try:
        #     req = urllib.request.urlopen('https://www.diretodostrens.com.br/api/status')
        #     data = json.loads(req.read().decode('utf-8'))
        # except urllib.error.HTTPError as err:
        #     logging.error('watcher > _updateDataStatus > HTTPError code: '+str(err.code))
        # except urllib.error.URLError as err:    
        #     logging.error('watcher > _updateDataStatus > Request error: '+str(err.reason))
        # except json.decoder.JSONDecodeError as err:
        #     logging.error('watcher > _updateDataStatus > JSON decode error: '+ str(err))
        # finally:
        #     if data != None:
        #         self._dataStatus = data
        #         for linha in self._dataStatus:
        #             if ('situacao' in linha) and (linha['situacao'] != 'Operação Normal'):
        #                 logging.debug(linha)

    def stop(self):
        self._running = False