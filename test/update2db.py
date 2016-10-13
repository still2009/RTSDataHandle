# coding=UTF-8
from TDPS import *
from DSPStruct import *
from db_process import *
from datetime import datetime as dt

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
# 上海全部订阅
def getAllSSEL1(conn):
    '''上海证券交易所分时数据'''
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,freq)
# 深圳全部订阅
def getAllSZSEL1(conn):
    '''深圳证券交易所分时数据'''
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
def unSubAll(conn):
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.unSubscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.unSubscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
def begin():
    conn = TDPS()
    createTable(engine)
    print('连接成功')
    getAllSSEL1(conn)
    print('上海订阅成功')
    getAllSZSEL1(conn)
    print('深圳订阅成功')
if __name__ == '__main__':
    begin()
