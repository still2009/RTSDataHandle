# coding:utf-8
from DSPStruct import Level1Min

from db import Session
from db_process import StatisticTask


def get_data():
    l = Level1Min()
    l.Freq = 60
    l.SecurityID = 1
    l.TradeTime = 12020202
    l.ProductID = 1
    l.Symbol = b'6000'
    l.TradingDate = b'2017-01-02'
    l.TradingTime = b'2017-01-02 14:36:00'
    l.UNIX = 0
    l.Market = b'SSE'
    l.ShortName = b'HAHA'
    l.OpenPrice = 11.4
    l.HighPrice = 11.5
    l.LowPrice = 11.2
    l.ClosePrice = 11.5
    l.Volume = 4545
    l.Amount = 45454545
    l.BenchMarkOpenPrice = 11.2
    l.Change = 343
    l.ChangeRatio = 344
    l.TotalVolume = 3434
    l.VWAP = 3434.88
    l.CumulativeLowPrice = 11.2
    l.CumulativeHighPrice = 11.5
    l.CumulativeVWAP = 345
    return l


def single_test():
    t = StatisticTask(Session)
    l = get_data()
    l.TradingTime = b'2017-01-02 14:36:00'
    t.add(l)
    l.TradingTime = b'2017-01-02 14:59:00'
    t.add(l)
    l.TradingTime = b'2017-01-02 09:30:00'
    t.add(l)
    print(t)
