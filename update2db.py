# coding=UTF-8
from TDPS import *
from DSPStruct import *
from db_process import *
from datetime import datetime as dt
import sys
from threading import current_thread

# 初始化2个线程
commitThread = ConsumeThread(Session)
itemCounter = Counter()
# 订阅回调函数，接收到数据是被调用，应该在该函数中处理接收到的数据。
def DB_MinCallBack(l):
    # 使用ProductID过滤中间数据,使用SecurityID过滤股票
    if l.SecurityID/1000000000 == 201 and l.ProductID != 4294967295:
        itemCounter.step()
        finalThread.add(l)

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
    print('启动子线程...')
    itemCounter.start()
    commitThread.start()
    print('创建数据库')
    createTable()
    print('开始订阅')
    ASub(conn,freq=f)

# 清理程序，并全部退订
def end(conn):
    print('关闭子线程...')
    itemCounter.stop()
    commitThread.stop()
    print('子线程关闭成功')
    AUnSub(conn)
    print('全部退订成功')

if __name__ == '__main__':
    begin(TDPS())
