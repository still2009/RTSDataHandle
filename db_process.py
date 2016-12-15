# coding:UTF-8
import time,sys,logging,threading,datetime
from datetime import timedelta
from db import *
import sqlalchemy,traceback
# 计数器类，从来展示数据实时接收的情况
class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.delta = 0
        self.count = 0
        self.runningFlag = True
    def run(self):
        print('计数器启动')
        while self.runningFlag:
            self.delta = self.count
            time.sleep(1)
            self.delta = self.count - self.delta
            sys.stdout.write('\r接收到的数据条目数：%s  每秒%s' % (self.count,self.delta))
            sys.stdout.flush()
    def stop(self):
        self.runningFlag = False
        print('收到线程退出指令,最终数据条数为%s条' % self.count)
    def reset(self):
        self.count = 0
    def step(self):
        self.count += 1

# 定时器任务类，用来执行定时任务
class DailyTask(threading.Thread):
    def __init__(self,h,m,s,fun,params):
        '''
        h : 小时 0~23
        m : 分钟 0~59
        fun : 执行的函数
        params : 函数参数
        '''
        threading.Thread.__init__(self)
        self.hour = h
        self.minute = m
        self.second = s
        self.fun = fun
        self.params = params
        self.runningFlag = True

    def _calcDelay(self):
        now = datetime.datetime.now()
        target = datetime.datetime(now.year,now.month,now.day,self.hour,self.minute,self.second)
        # 今日此时已过
        if(target < now):
            target = now + timedelta(days=1)
        return abs((target-now).total_seconds())

    def run(self):
        while(self.runningFlag):
            delay = self._calcDelay()
            print('设定在%ss后执行任务\n' % delay)
            time.sleep(delay)
            print('开始执行任务..')
            self.fun(*self.params)
            print('任务执行结束..')

    def stop(self):
        self.runningFlag = False

class StatisticTask(threading.Thread):
    def __init__(self,SessionClass):
        threading.Thread.__init__(self)
        self.SessionClass = SessionClass
        self.reset()

    def reset(self):
        self.openPrc = {}
        self.tradePrc = {}
        self.otherPrc = {}
        self.dbSession = self.SessionClass()
        self.runningFlag = True
        self.commitingFlag = False
    def add(self,l):
        hour = int(l.TradingTime[11:13])
        minute = int(l.TradingTime[14:16])
        if(hour == 14 and 36 <= minute <= 45):
            if self.otherPrc.get(l.SecurityID) != None:
                self.otherPrc[l.SecurityID].HIGH = max(l.HighPrice,self.otherPrc[l.SecurityID].HIGH)
                self.otherPrc[l.SecurityID].LOW = min(l.HighPrice,self.otherPrc[l.SecurityID].LOW)
                self.otherPrc[l.SecurityID].SIGNAL = self.otherPrc[l.SecurityID].SIGNAL + (l.HighPrice + l.LowPrice)/20
                self.otherPrc[l.SecurityID].DELAY = int(time.time()) - l.UNIX/1000
            else:
                self.otherPrc[l.SecurityID] = L2OtherPrice(l)
        elif(hour == 14 and 51 <= minute <= 59 or hour+minute == 15):
            if self.tradePrc.get(l.SecurityID) != None:
                self.tradePrc[l.SecurityID].PRICE = self.tradePrc[l.SecurityID].PRICE + (l.HighPrice + l.LowPrice)/20
                self.tradePrc[l.SecurityID].DELAY = int(time.time()) - l.UNIX/1000
            else:
                self.tradePrc[l.SecurityID] = L2TradePrice(l)
        elif(hour == 9 and minute == 30):
            if self.openPrc.get(l.SecurityID) != None:
                self.openPrc[l.SecurityID].PRICE = l.OpenPrice
                self.openPrc[l.SecurityID].DELAY = int(time.time()) - l.UNIX/1000
            else:
                self.openPrc[l.SecurityID] = L2OpenPrice(l)

    def commit():
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        if(hour == 14 and minute == 45 and second >= 15):
            self.dbSession.add_all([self.otherPrc[i] for i in self.otherPrc])
            self.dbSession.commit()
        elif(hour+minute == 15 and second >= 15):
            self.dbSession.add_all([self.tradePrc[i] for i in self.tradePrc])
            self.dbSession.commit()
        elif(hour == 9 and minute == 30 and second >= 15):
            self.dbSession.add_all([self.openPrc[i] for i in self.openPrc])
            self.dbSession.commit()

    def run(self):
        while(self.runningFlag):
            self.commitingFlag = True
            self.commit()
            self.commitingFlag = False
            time.sleep(1)
    def stop(self):
        self.runningFlag = False
        while(True):
            if(not self.commitingFlag):
                time.sleep(2)
                break
            time.sleep(1)
        print('task线程停止')
        self.reset()
        print('task线程重置')
