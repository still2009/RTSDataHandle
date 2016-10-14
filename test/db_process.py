# coding:UTF-8
import threading
import time
from db import *
import logging

logFname = 'thread_%s.log' % datetime.datetime.now().strftime('%y_%m_%d-%H:%M:%S')
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%b %d  %H:%M:%S',
                filename=logFname,
                filemode='w')
def log(txt):
    logging.info(txt)
class ConsumeThread(threading.Thread):
    '''数据消费线程'''
    def __init__(self,type,SessionClass,finalDelay=35,middleDelay=15):
        '''
        type 代表线程类型，有两种：
        1. 最终分时数据 -> final
        2. 中间分时数据 -> middle
        最终分时数据将会被优先写入数据库
        '''
        threading.Thread.__init__(self)
        self.Priority = 1 if type == 'final' else 0
        self.delay = finalDelay if self.Priority == 1 else middleDelay
        self.SessionClass = SessionClass
        self.dbSession = SessionClass()

        self.AddFlag = True
    def run(self):
        log('p:%s Started' % self.Priority)
        while True:
            time.sleep(self.delay)
            # 开始换session
            self.AddFlag = False
            sLen = len(self.dbSession.new)
            if sLen <= 0:
                log('p-%s empty!!' % self.Priority)
                continue
            s = self.dbSession
            self.dbSession = self.SessionClass()
            self.AddFlag = True
            # 换session成功
            log('p:%s is commiting %s items' % (self.Priority,sLen))
            s.commit()
            log('p:%s commited %s items' % (self.Priority,sLen))
            s.close()
    def add(self,data):
        while True:
            if self.AddFlag:
                self.dbSession.add(Str2MinuteData(data))
                break
