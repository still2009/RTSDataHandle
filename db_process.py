# coding:UTF-8
import datetime
import logging
import sys
import threading
from datetime import timedelta

from db import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%d %b %Y %H:%M:%S',
                    filename='receiver.log',
                    filemode='w')


# 计数器类，展示数据实时接收情况
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
            sys.stdout.write('\r接收到的数据条目数：%s  每秒%s' % (self.count, self.delta))
            sys.stdout.flush()

    def stop(self):
        self.runningFlag = False
        print('收到线程退出指令,最终数据条数为%s条' % self.count)

    def reset(self):
        self.count = 0

    def step(self):
        self.count += 1


# 自动化控制类，根据配置文件 控制 数据接收的开与关
class MonitorTask(threading.Thread):
    def __init__(self, bf, bp, ef, ep):
        """
        bf : begin function 起始任务执行的函数
        bp : begin function params起始函数参数
        ef : 结束任务函数
        ep : 结束任务函数参数
        """
        threading.Thread.__init__(self)
        self.runningFlag = True
        self.reloadConf()
        self.bf = bf
        self.bp = bp
        self.ef = ef
        self.ep = ep
        self.beginFlag = False  # 指示begin函数是否在运行中

    def reloadConf(self):
        """重新加载配置"""
        timeConf = json.load(open('conf/timer.conf', 'r'))
        self.startTime = (timeConf['start_h'], timeConf['start_m'], timeConf['start_s'])
        self.endTime = (timeConf['end_h'], timeConf['end_m'], timeConf['end_s'])

    def _calcDelay(self):
        """
        比较当前时间与配置时间，并决定begin和end函数的执行时间
        若在开盘时间内，则执行begin函数，若已收盘，则执行end函数
        return (delay1,delay2)，延时元祖
        """
        now = datetime.datetime.now()
        tgtBegin = datetime.datetime(now.year, now.month, now.day, self.startTime[0], self.startTime[1],
                                     self.startTime[2])
        tgtEnd = datetime.datetime(now.year, now.month, now.day, self.endTime[0], self.endTime[1], self.endTime[2])
        if (tgtBegin < now < tgtEnd):  # 盘中
            return (0, (tgtEnd - now).total_seconds())
        elif (now > tgtEnd):  # 盘后
            tgtBegin = tgtBegin + timedelta(days=1)
            return ((tgtBegin - now).total_seconds(), 0)
        elif (now < tgtBegin):  # 盘前
            return ((tgtBegin - now).total_seconds(), 0)
        else:
            time.sleep(1)
            return self._calcDelay()

    def run(self):
        '''根据延时执行任务'''
        while (self.runningFlag):
            delay = self._calcDelay()
            if self.beginFlag:
                # 起始函数运行时的操作,begin与end是一一对应的
                time.sleep(delay[1])
                self.ef(*self.ep)
                self.beginFlag = False
            else:
                # 在任何时刻，当begin不在运行中时，执行end都是毫无意义的，end总是在begin之后运行
                time.sleep(delay[0])
                self.beginFlag = True
                self.bf(*self.bp)

    def stop(self):
        self.runningFlag = False


# 数据统计类，根据需求对实时接收到的数据进行统计并提交到数据库
class StatisticTask(threading.Thread):
    def __init__(self, SessionClass):
        threading.Thread.__init__(self)
        self.SessionClass = SessionClass
        self.reset()
        self.addFlag = True

    def reset(self):
        self.openPrc = {}
        self.tradePrc = {}
        self.otherPrc = {}
        self.dbSession = self.SessionClass()
        self.runningFlag = True
        self.commitingFlag = False

    def add(self, l):
        if not self.addFlag:
            return
        hour = int(l.TradingTime[11:13])
        minute = int(l.TradingTime[14:16])
        if hour == 14 and 36 <= minute <= 45:
            logging.info('14:36--14:45 : %s' % l.ProductID)
            if self.otherPrc.get(l.SecurityID) is not None:  # 已经计算过一条了
                self.otherPrc[l.SecurityID].HIGH = max(l.CumulativeHighPrice, self.otherPrc[l.SecurityID].HIGH)
                self.otherPrc[l.SecurityID].LOW = min(l.CumulativeLowPrice, self.otherPrc[l.SecurityID].LOW)
                prevPrc = float(self.otherPrc[l.SecurityID].SIGNAL)
                self.otherPrc[l.SecurityID].SIGNAL = prevPrc + (l.HighPrice + l.LowPrice) / 20
                self.otherPrc[l.SecurityID].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.otherPrc[l.SecurityID].PID += 1  # 通过起始ProductID每计算一次加一来判断计算条目是否齐全
            else:
                self.otherPrc[l.SecurityID] = L2OtherPrice(l)
        elif hour == 14 and 51 <= minute <= 59 or (hour == 15 and minute == 0):
            logging.info('14:51--15:00 : %s' % l.ProductID)
            if self.tradePrc.get(l.SecurityID) is not None:
                prevPrc = float(self.tradePrc[l.SecurityID].PRICE)
                self.tradePrc[l.SecurityID].PRICE = prevPrc + (l.HighPrice + l.LowPrice) / 20
                self.tradePrc[l.SecurityID].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.tradePrc[l.SecurityID].PID += 1
            else:
                self.tradePrc[l.SecurityID] = L2TradePrice(l)
        elif hour == 9 and minute == 30:
            logging.info('9:30 : %s' % l.ProductID)
            if self.openPrc.get(l.SecurityID) is not None:
                self.openPrc[l.SecurityID].PRICE = l.OpenPrice
                self.openPrc[l.SecurityID].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.openPrc[l.SecurityID].PID += 1
            else:
                self.openPrc[l.SecurityID] = L2OpenPrice(l)

    def commit(self):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        if hour == 14 and minute == 45 and second >= 15:
            self.dbSession.add_all([self.otherPrc[i] for i in self.otherPrc])
            self.dbSession.commit()
        elif hour == 15 and minute == 0 and second >= 15:
            self.dbSession.add_all([self.tradePrc[i] for i in self.tradePrc])
            self.dbSession.commit()
        elif hour == 9 and minute == 30 and second >= 15:
            self.dbSession.add_all([self.openPrc[i] for i in self.openPrc])
            self.dbSession.commit()

    def run(self):
        while self.runningFlag:
            self.commitingFlag = True
            self.commit()
            self.commitingFlag = False
            time.sleep(1)

    def stop(self):
        self.runningFlag = False
        while True:
            if not self.commitingFlag:
                time.sleep(2)
                break
            time.sleep(1)
        print('task线程停止')
        self.reset()
        print('task线程重置')
