# coding=UTF-8
from TDPS import *
from DSPStruct import *
import time
from db import *

# 分时数据,额外增加receive_unix,ReceiveDate
def DB_MinCallBack(Level1Min):
    data = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(Level1Min.Freq,
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
           datetime.datetime().now().strftime('%Y-%m-%d %H:%M:%S'))
    save(data,getSession())


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

if __name__ == '__main__':
    conn = TDPS()
    print('连接成功')
    getAllSSEL1(conn)
    getAllSZSEL1(conn)