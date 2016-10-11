# coding=UTF-8
from file import *
import datetime

fileUtil = FileUtil()

# 上海分时数据,额外增加receive_unix,receiveDate
def SSEL1MinCallBack(Level1Min):
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
           datetime.datetime().now().strftime('%Y-%m-%d %H:%M:%S'))
    fileUtil.Save(4113,Level1Min.Freq,data)

# 深圳分时数据,额外增加receive_unix,receiveDate
def SZSEL1MinCallBack(Level1Min):
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
           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    fileUtil.Save(8209,Level1Min.Freq,data)
