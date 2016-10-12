# coding=UTF-8
from TDPS import *
from DSPStruct import *
from db import *
from datetime import datetime as dt

# 分时数据,额外增加receive_unix,ReceiveDate
def DB_MinCallBack(Level1Min):
    rd = dt.now().strftime('%Y-%m-%d %H:%M:%S')
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
    save(data,getSession())

# 综合数据订阅函数
def ASub(code=b'*',freq=-1,market='A'):
    freqs = [freq] if freq != -1 else [60,300,600,900,1800,3600]
    if market == 'A' or market == 'SH':
        for freq in freqs:
            conn = TDPS()
            conn.RegSSEL1MinCallBack(DB_MinCallBack) # 上海回调注册
            conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
    if market == 'A' or market == 'SZ':
        for freq in freqs:
            conn = TDPS()
            conn.RegSZSEL1MinCallBack(DB_MinCallBack) # 深圳回调注册
            conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
# 综合数据退订函数
def AUnSub(conn):
    conn.RegSSEL1MinCallBack(DB_MinCallBack)
    conn.RegSZSEL1MinCallBack(DB_MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.unSubscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
def begin():
    ASub()
if __name__ == '__main__':
    begin()
