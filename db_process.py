# coding:UTF-8
# import multiprocessing
import threading
import time
from db import *
import logging
import sys

class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.delta = 0
        self.count = 0
        self.runningFlag = True
    def run(self):
        print('counter started')
        while self.runningFlag:
            self.delta = self.count
            time.sleep(1)
            self.delta = self.count - self.delta
            sys.stdout.write('\r接收到的数据条目数：%s  每秒%s' % (self.count,self.delta))
            sys.stdout.flush()
    def stop(self):
        self.runningFlag = False
        print('收到线程推出制定,最终数据条数为%s条' % self.count)
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
        self.runningFlag = True
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
        '''
        定时commit session中待提交的数据事务
        由于commit本身需要时间，而此时CallBack依然会add数据
        所以需要新的session来负责，故有换session的操作。
        '''
        self.log('p:%s Started' % self.Priority)
        while self.runningFlag:
            time.sleep(self.delay)
            # 判断是否为空，无需换session
            sLen = len(self.dbSession.new)
            if sLen <= 0:
                self.log('p-%s empty!!' % self.Priority)
                continue
            # 开始换session
            self.AddFlag = False
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
    def stop(self):
        self.runningFlag = False
        time.sleep(1)
        sLen = len(self.dbSession.new)
        print('发出停止线程的指令,正在进行最后的commit，条数为%s条' % sLen)
        self.dbSession.commit()
