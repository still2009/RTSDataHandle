# coding=UTF-8
from TDPS import *
from DSPStruct import *
from db_process import *
from datetime import datetime as dt
import sys
from threading import current_thread

# 初始化2个线程
finalThread = ConsumeThread('final',Session)
middleThread = ConsumeThread('middle',Session)
itemCounter = Counter()
# 分时数据,额外增加receive_unix,ReceiveDate
def DB_MinCallBack(Level1Min):
    nowUNIX = time.time()
    rd = dt.fromtimestamp(nowUNIX).strftime('%Y-%m-%d %H:%M:%S')
    data = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(Level1Min.Freq,
           Level1Min.SecurityID,
           Level1Min.TradeTime,
           Level1Min.ProductID,
           Level1Min.Symbol,
           Level1Min.TradingDate,
           Level1Min.TradingTime,
           Level1Min.UNIX,
           Level1Min.Market,
           Level1Min.ShortName.decode("UTF8"),
           Level1Min.OpenPrice,
           Level1Min.HighPrice,
           Level1Min.LowPrice,
           Level1Min.ClosePrice,
           Level1Min.Volume,
           Level1Min.Amount,
           Level1Min.BenchMarkOpenPrice,
           Level1Min.Change,
           Level1Min.ChangeRatio,
           Level1Min.TotalVolume,
           Level1Min.VWAP,
           Level1Min.CumulativeLowPrice,
           Level1Min.CumulativeHighPrice,
           Level1Min.CumulativeVWAP,
           time.time(),
           rd)
    td = finalThread if Level1Min.UNIX <= int(1000*nowUNIX) else middleThread
    itemCounter.step()
    td.add(data)

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
    if market == 'A' or market == 'SZ':
        for freq in freqs:
            conn.RegSZSEL1MinCallBack(DB_MinCallBack) # 深圳回调注册
            conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
# 综合数据退订函数
def AUnSub(conn):
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.unSubscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
def begin(f=60):
    print('任务开始执行...')
    itemCounter.start()
    finalThread.start()
    middleThread.start()
    print('创建数据库')
    createTable()
    ASub(TDPS(),freq=f)
def end():
    print('任务结束执行...')
    itemCounter.stop()
    finalThread.stop()
    middleThread.stop()
    print('子线程全部关闭')
    AUnSub(TDPS())
    print('全部退订')
if __name__ == '__main__':
    fq = 0
    if len(sys.argv) != 2:
        print('usage: python update2db.py 60\n60 即分时频率秒数为60\n默认为60')
        fq = 60
    else:
        fq = int(sys.argv[1])
    begin(fq)
