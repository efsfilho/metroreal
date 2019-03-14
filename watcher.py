import time
import json
import schedule
import urllib.request
from threading import Thread

# status = [{"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:00.334477Z", "criado": "2019-02-19T07:41:00.803549Z", "codigo": 1, "id": 5098819247144960}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:00.337420Z", "criado": "2019-02-19T07:41:00.858902Z", "codigo": 2, "id": 6289236323991552}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:00.340037Z", "criado": "2019-02-19T07:41:00.877520Z", "codigo": 3, "id": 5698936018829312}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:01.269863Z", "criado": "2019-02-19T07:41:00.804018Z", "codigo": 4, "id": 5714949670174720}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:01.152332Z", "criado": "2019-02-19T08:50:01.445111Z", "codigo": 5, "id": 5135986065408000}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.744557Z", "criado": "2019-02-19T07:01:01.103122Z", "codigo": 7, "id": 5709513986408448}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.755445Z", "criado": "2019-02-19T08:32:00.127045Z", "codigo": 8, "id": 5650211980443648}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.831433Z", "criado": "2019-02-19T07:01:01.207293Z", "codigo": 9, "id": 5641694707974144}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.834635Z", "criado": "2019-02-19T07:01:01.305430Z", "codigo": 10, "id": 5089750893461504}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.837476Z", "criado": "2019-02-19T07:01:01.356346Z", "codigo": 11, "id": 5675522809921536}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.839961Z", "criado": "2019-02-19T07:01:01.441655Z", "codigo": 12, "id": 5651304160428032}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:16.842331Z", "criado": "2019-02-19T07:01:01.524086Z", "codigo": 13, "id": 5728427093000192}, {"situacao": "Operação Normal", "modificado": "2019-02-19T14:09:00.342879Z", "criado": "2019-02-19T07:41:00.932501Z", "codigo": 15, "id": 5678845319446528}]
status = []

def dateformat(dt):
    return time.strftime("%a, %d %b %Y %H:%M:%S", dt)

def writeJson(data):    
    with open('data.json', 'a', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write('\n')

def getData():
    global status
    data = urllib.request.urlopen('https://www.diretodostrens.com.br/api/status').read()
    status = json.loads(data.decode('utf-8'))
    strdatetime = dateformat(time.gmtime())
    print(strdatetime)
    for linha in status:
        if ('situacao' in linha) and (linha['situacao'] != 'Operação Normal'):
            writeJson(linha)

# schedule.every(30).minutes.do(getData)
# schedule.every(10).seconds.do(getData)


class Watcher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.running = False

    def run(self):
        if self.running:
            return
        self.running = True
        while self.running:
            schedule.run_pending()
            time.sleep(1)
        self.running = False
        print('thread finished')

    def addJob(self, job):
        schedule.every(4).seconds.do(job)
    def clear(self, tag=None):
        schedule.clear(tag)
    def cancel(self):
        schedule.cancel_job()
    def stop(self):
        self.running = False