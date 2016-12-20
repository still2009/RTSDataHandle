# coding=UTF-8
from TDPS import *
from DSPStruct import *
from db_process import *
from datetime import datetime as dt
import sys,math
from threading import current_thread

#声明全局变量
itemCounter = None
task = None
# 订阅回调函数，接收到数据是被调用，应该在该函数中处理接收到的数据。
def DB_MinCallBack(l):
    global itemCounter,task
    # 先丢弃修正数据(mintime在当前时间之前)
    now = dt.now()
    hour = int(l.TradingTime[11:13])
    minute = int(l.TradingTime[14:16])
    # 丢弃修正数据
    if hour < now.hour or (hour == now.hour and minute < now.minute):
        return
    # 使用ProductID过滤中间数据,使用SecurityID过滤股票
    if math.floor(l.SecurityID/1000000000) == 201 and l.ProductID != 4294967295:
        itemCounter.step()
        task.add(l)

# 上海单支订阅
def getSSEL1(conn,code):
    # 上海证券交易所每1min股票数据
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
# 深圳单支订阅
def getSZSEL1(conn,code):
    # 深圳证券交易所每1min股票数据
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,freq)
# 综合数据订阅函数
def ASub(conn,code=b'*',freq=-1,market='A'):
    freqs = [freq] if freq != -1 else [60,300,600,900,1800,3600]
    if market == 'A' or market == 'SH':
        for freq in freqs:
            conn.RegSSEL1MinCallBack(DB_MinCallBack) # 上海回调注册
            conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
        print('上海订阅成功')
    if market == 'A' or market == 'SZ':
        for freq in freqs:
            conn.RegSZSEL1MinCallBack(DB_MinCallBack) # 深圳回调注册
            conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,freq)
        print('深圳订阅成功')
# 综合数据退订函数
def AUnSub(conn):
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.unSubscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)

# 初始化程序，并开启沪深全市场1min订阅
def begin(conn,f=60):
    # 初始化2个线程
    global itemCounter,task
    itemCounter = Counter()
    task = StatisticTask(Session)
    # 创建表
    print('创建表')
    createTables()
    print('启动子线程...')
    itemCounter.start()
    task.start()
    print('开始订阅')
    ASub(conn,freq=f)

# 清理程序，并全部退订
def end(conn):
    AUnSub(conn)
    print('全部退订成功')
    print('关闭子线程...')
    global itemCounter,task
    itemCounter.stop()
    task.stop()
    print('子线程关闭成功')
    print('删除表')
    dropTables()


# 初始化计时线程
globalConn = TDPS()
timeConf = json.load(open('timer.conf','r'))
dailyStart = DailyTask(timeConf['start_h'],timeConf['start_m'],timeConf['start_s'],begin,(globalConn,))
dailyEnd = DailyTask(timeConf['end_h'],timeConf['end_m'],timeConf['end_s'],end,(globalConn,))
if __name__ == '__main__':
    dailyStart.start()
    dailyEnd.start()
