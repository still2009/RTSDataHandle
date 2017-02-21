# coding:UTF-8
import datetime
import sys
import threading
from datetime import timedelta

from dthandle.models import *


# 计数器类，展示数据实时接收情况
class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.delta = 0
        self.count = 0
        self.runningFlag = True

    def run(self):
        logging.info('计数器启动')
        while self.runningFlag:
            self.delta = self.count
            time.sleep(1)
            self.delta = self.count - self.delta
            sys.stdout.write('\r接收到的数据条目数：%s  每秒%s' % (self.count, self.delta))
            sys.stdout.flush()

    def stop(self):
        self.runningFlag = False
        logging.info('最终数据条数为%s条,计数器停止' % self.count)

    def reset(self):
        self.count = 0

    def step(self):
        self.count += 1


# 自动化控制类，根据配置文件 控制 数据接收的开与关
class MonitorTask(threading.Thread):
    def __init__(self, bf, bp, ef, ep):
        """
        bf : start_receiver function 起始任务执行的函数
        bp : start_receiver function params起始函数参数
        ef : 结束任务函数
        ep : 结束任务函数参数
        """
        threading.Thread.__init__(self)
        self.runningFlag = True
        self.reload_conf()
        self.bf = bf
        self.bp = bp
        self.ef = ef
        self.ep = ep
        self.beginFlag = False  # 指示begin函数是否在运行中

    def reload_conf(self):
        """重新加载配置"""
        self.startTime = (gconf['start_h'], gconf['start_m'], gconf['start_s'])
        self.endTime = (gconf['end_h'], gconf['end_m'], gconf['end_s'])

    def _calc_delay(self):
        """
        比较当前时间与配置时间，并决定begin和end函数的执行时间
        若在开盘时间内，则执行begin函数，若已收盘，则执行end函数
        return (delay1,delay2)，延时元祖
        """
        now = datetime.datetime.now()
        tgtBegin = datetime.datetime(now.year, now.month, now.day, self.startTime[0], self.startTime[1],
                                     self.startTime[2])
        tgtEnd = datetime.datetime(now.year, now.month, now.day, self.endTime[0], self.endTime[1], self.endTime[2])
        if tgtBegin < now < tgtEnd:  # 盘中
            return 0, (tgtEnd - now).total_seconds()
        elif now > tgtEnd:  # 盘后
            tgtBegin = tgtBegin + timedelta(days=1)
            return (tgtBegin - now).total_seconds(), 0
        elif now < tgtBegin:  # 盘前
            return (tgtBegin - now).total_seconds(), 0
        else:
            time.sleep(1)
            return self._calc_delay()

    def run(self):
        """根据延时执行任务"""
        while self.runningFlag:
            delay = self._calc_delay()
            if self.beginFlag:
                # 起始函数运行时的操作,begin与end是一一对应的
                logging.info('%s 秒之后停止接收' % delay[1])
                time.sleep(delay[1])
                self.ef(*self.ep)
                self.beginFlag = False
            else:
                # 在任何时刻，当begin不在运行中时，执行end都是毫无意义的，end总是在begin之后运行
                logging.info('%s 秒之后开始接收' % delay[0])
                time.sleep(delay[0])
                self.beginFlag = True
                self.bf(*self.bp)

    def stop(self):
        """终止run方法以销毁线程"""
        self.runningFlag = False


# 数据统计类，根据需求对实时接收到的数据进行统计并提交到数据库
class StatisticTask(threading.Thread):
    def __init__(self, session_class):
        """
        线程初始化
        tradePrc为一个map,例如:
        {'6000' : (Level1Min, lastProductID, firstProductID),
        '9000' : (Level1Min, lastProductID, firstProductID)}
        """
        threading.Thread.__init__(self)
        self.SessionClass = session_class
        self.openPrc = {}
        self.tradePrc = {}
        self.otherPrc = {}
        self.dbSession = self.SessionClass()
        self.runningFlag = True

    def add(self, l):
        """在线程运行期间 被回调函数的调用 添加数据至线程的容器中"""
        if not self.runningFlag:
            logging.info('统计线程已经关闭,不再添加数据')
            return
        hour = int(l.TradingTime[11:13])
        minute = int(l.TradingTime[14:16])
        # 第一个时间分段PID 217-226
        if hour == 14 and 36 <= minute <= 45:
            if self.otherPrc.get(l.SecurityID) is not None:  # 已经计算过一条了
                if self.otherPrc[l.SecurityID][1] == l.ProductID:  # 上一次计算的id不该等于这次的
                    return
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-otherPrc : %s %s:%s-%s-%s' %
                                  (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                                  )
                self.otherPrc[l.SecurityID][0].HIGH = max(l.CumulativeHighPrice, self.otherPrc[l.SecurityID][0].HIGH)
                self.otherPrc[l.SecurityID][0].LOW = min(l.CumulativeLowPrice, self.otherPrc[l.SecurityID][0].LOW)
                prev_prc = float(self.otherPrc[l.SecurityID][0].SIGNAL)
                self.otherPrc[l.SecurityID][0].SIGNAL = prev_prc + (l.HighPrice + l.LowPrice) / 20
                self.otherPrc[l.SecurityID][0].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.otherPrc[l.SecurityID][0].PID += 1  # 通过起始ProductID每计算一次加一来判断计算条目是否齐全
                self.otherPrc[l.SecurityID][1] = l.ProductID
            else:
                self.otherPrc[l.SecurityID] = [l2model_other(l), l.ProductID, l.ProductID]
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-otherPrc : %s %s:%s-%s-%s' %
                              (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                              )
        # 第二个时间段PID 232-241
        elif hour == 14 and 51 <= minute <= 59 or (hour == 15 and minute == 0):
            if self.tradePrc.get(l.SecurityID) is not None:
                if self.tradePrc[l.SecurityID][1] == l.ProductID:
                    return
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-tradePrc : %s %s:%s-%s-%s' %
                                  (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                                  )
                prev_prc = float(self.tradePrc[l.SecurityID][0].PRICE)
                self.tradePrc[l.SecurityID][0].PRICE = prev_prc + (l.HighPrice + l.LowPrice) / 20
                self.tradePrc[l.SecurityID][0].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.tradePrc[l.SecurityID][0].PID += 1
                self.tradePrc[l.SecurityID][1] = l.ProductID
            else:
                self.tradePrc[l.SecurityID] = [l2model_trade(l), l.ProductID, l.ProductID]
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-tradePrc : %s %s:%s-%s-%s' %
                              (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                              )
        # 开盘
        elif hour == 9 and minute == 30:
            if self.openPrc.get(l.SecurityID) is not None:
                if self.openPrc[l.SecurityID][1] == l.ProductID:
                    return
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-openPrc : %s %s:%s-%s-%s' %
                                  (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                                  )
                self.openPrc[l.SecurityID][0].PRICE = l.OpenPrice
                self.openPrc[l.SecurityID][0].DELAY = int(time.time()) - int(l.UNIX / 1000)
                self.openPrc[l.SecurityID][0].PID += 1
                self.openPrc[l.SecurityID][1] = l.ProductID
            else:
                self.openPrc[l.SecurityID] = [l2model_open(l), l.ProductID, l.ProductID]
                if int(l.Symbol) in gconf['log_symbol']:  # 日志记录一支股票的计算过程
                    logging.debug('%s-openPrc : %s %s:%s-%s-%s' %
                                  (l.Symbol, l.ProductID, hour, minute, l.HighPrice, l.LowPrice)
                                  )

    def run(self):
        """在指定时间提交数据到数据库"""
        while self.runningFlag:
            now = datetime.datetime.now()
            hour, minute, second = now.hour, now.minute, now.second
            # 开盘价写入
            if hour == 9 and minute == 30 and second >= 15:
                self.dbSession.add_all([self.openPrc[i][0] for i in self.openPrc])
                self.dbSession.commit()
            # signal价写入
            elif hour == 14 and minute == 45 and second >= 15:
                self.dbSession.add_all([self.otherPrc[i][0] for i in self.otherPrc])
                self.dbSession.commit()
            # trade价写入
            elif hour == 15 and minute == 0 and second >= 15:
                self.dbSession.add_all([self.tradePrc[i][0] for i in self.tradePrc])
                self.dbSession.commit()
            time.sleep(1)
        logging.info('统计线程停止')

    def stop(self):
        """终止run方法以销毁线程"""
        self.runningFlag = False

    def __str__(self):
        return '%s %s %s' % (str(self.openPrc), str(self.otherPrc), str(self.tradePrc))
