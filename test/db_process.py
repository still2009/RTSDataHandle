# coding:UTF-8
import threading
import time
from db import *

class ConsumeThread(threading.Thread):
    '''数据消费线程'''
    def __init__(self,type):
        ''''
        type 代表线程类型，有两种：
        1. 最终分时数据 -> final
        2. 中间分时数据 -> middle
        最终分时数据将会被优先写入数据库
        ''''
        threading.Thread.__init__(self)
        self.Priority = 1 if type == 'final' else 0
        self.delay = 15 if self.Priority == 1 else 150
        self.dbSession = Session()
    def run(self):
         while not self.thread_stop:
             while True:
                time.sleep(self.delay)
                self.dbSession.commit()
    def add(self,data):
        self.dbSession.add(Str2MinuteData(data))

finalThread = ConsumeThread('final')
middleThread = ConsumeThread('middle')
finalThread.start()
middleThread.start()
