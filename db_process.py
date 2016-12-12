# coding:UTF-8
import time,sys,logging,threading,datetime
from datetime import timedelta
from db import *

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

# 数据消费线程类，用来将接收到的数据存储到session并最终提交到数据库
class ConsumeThread(threading.Thread):
    '''数据消费线程'''
    def __init__(self,SessionClass,delay = 6):
        '''
        SessionClass为生成Session的类
        delay为提交延时
        '''
        threading.Thread.__init__(self)
        self.runningFlag = True
        self.commitingFlag = False
        self.delay = delay
        self.SessionClass = SessionClass
        self.dbSession = SessionClass()
        self.AddFlag = True
        self.logger = logging.getLogger('提交线程')
        self.logger.setLevel(logging.INFO)
        logFname = './数据库提交线程日志%s.log' % datetime.datetime.now().strftime('%y%m%d %H_%M_%S')
        fh = logging.FileHandler(logFname)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log(self,txt):
        self.logger.info(txt)

    def run(self):
        '''
        定时提交session的插入事务
        由于commit本身需要时间，而此时CallBack依然会add数据
        所以需要新的session来负责，故有换session的操作。
        '''
        self.log('数据库提交线程 开始启动...')
        while self.runningFlag:
            time.sleep(self.delay)
            # 判断是否为空，无需换session
            sLen = len(self.dbSession.new)
            if sLen <= 0:
                self.log('session为空，无需提交')
                continue
            # 开始换session
            self.AddFlag = False
            s = self.dbSession
            self.dbSession = self.SessionClass()
            self.AddFlag = True
            # 换session成功
            self.commitingFlag = True
            self.log('开始提交 %s 条数据' % sLen)
            s.commit()
            self.log('提交 %s 条完成' % sLen)
            s.close()
            self.commitingFlag = False

    def add(self,data):
        '''
        将接收到的一条数据转换为ORM对象，并添加到数据库的session中
        该函数被行情订阅的callback函数持续调用
        '''
        while self.runningFlag:
            if self.AddFlag:
                self.dbSession.add(Level1Min2MinuteData(data))
                break
            time.sleep(0.2)

    def stop(self):
        self.runningFlag = False
        time.sleep(1)
        # 等待一秒，确保主循环换了新的session，无论之前的session有没有提交完

        sLen = len(self.dbSession.new)
        self.log('准备停止提交数据，正在进行最后的commit，条数为%s' % sLen)
        self.dbSession.commit()
        self.log('最后一次提交成功，条数为%s' % sLen)
        while(True):
            if(not self.commitingFlag):
                self.log('所有session提交完成，线程停止工作')
                break
            time.sleep(1)

# 定时器任务类，用来执行定时任务
class DailyTask(threading.Thread):
    def __init__(self,h,m,fun,params):
        '''
        h : 小时 0~23
        m : 分钟 0~59
        fun : 执行的函数
        params : 函数参数
        '''
        threading.Thread.__init__(self)
        self.hour = h
        self.minute = m
        self.fun = fun
        self.params = params
        self.runningFlag = True

    def _calcDelay(self):
        now = datetime.datetime.now()
        target = (now.year,now.month,now.day,self.hour,self.minute)
        # 今日此时已过
        if(target > now):
            target = now + timedelta(days=1)
        return abs((target-now).total_seconds())

    def run(self):
        while(self.runningFlag):
            time.sleep(self._calcDelay())
            self.fun(*self.params)

    def stop(self):
        self.runningFlag = False
