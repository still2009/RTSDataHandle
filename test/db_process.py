# coding:UTF-8
# import multiprocessing
import threading
import time
from db import *
import logging

class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.count = 0
    def run(self):
        while True:
            time.sleep(5)
            print('接收到的数据条目数：%s' % self.count)
    def reset(self):
        self.count = 0
    def step(self):
        self.count += 1

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
        self.logger = logging.getLogger('p:%s thread' % self.Priority)
        self.logger.setLevel(logging.INFO)
        logFname = './thread_%s_%s.log' % (self.Priority,datetime.datetime.now().strftime('%y%m%d_%H_%M_%S'))
        fh = logging.FileHandler(logFname)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    def log(self,txt):
        self.logger.info(txt)
    def run(self):
        self.log('p:%s Started' % self.Priority)
        while True:
            time.sleep(self.delay)
            # 开始换session
            self.AddFlag = False
            sLen = len(self.dbSession.new)
            if sLen <= 0:
                self.log('p-%s empty!!' % self.Priority)
                continue
            s = self.dbSession
            self.dbSession = self.SessionClass()
            self.AddFlag = True
            # 换session成功
            self.log('p:%s is commiting %s items' % (self.Priority,sLen))
            s.commit()
            self.log('p:%s commited %s items' % (self.Priority,sLen))
            s.close()
    def add(self,data):
        while True:
            if self.AddFlag:
                self.dbSession.add(Str2MinuteData(data))
                break
