# coding:utf-8
import random
import time
from datetime import datetime, timedelta

from DSPStruct import Level1Min

from dthandle.models import GSession
from dthandle.models import l2model_open
from dthandle.tasks import StatisticTask


# 构造一条用于测试的股票数据
def create_item(pid, trade_time, symbol=600000):
    l = Level1Min()
    l.Freq = 60
    l.SecurityID = 200001
    l.ProductID = pid
    l.Symbol = bytes(str(symbol), encoding='utf-8')
    l.TradingDate = bytes(trade_time.strftime('%Y-%m-%d'), encoding='utf-8')
    l.TradingTime = bytes(trade_time.strftime('%Y-%m-%d %H:%M:%S'), encoding='utf-8')
    l.TradeTime = int(time.mktime(trade_time.timetuple()))
    l.UNIX = l.TradeTime  # 此处与实际稍有不同
    l.Market = b'SSE'
    l.ShortName = b'test_name'
    l.OpenPrice = random.uniform(10, 20)
    l.HighPrice = float(random.uniform(10, 20))
    l.LowPrice = float(random.uniform(10, 20))
    l.ClosePrice = random.uniform(10, 20)
    l.Volume = random.randint(100, 200)
    l.Amount = random.randint(100, 200)
    l.BenchMarkOpenPrice = random.uniform(10, 20)
    l.Change = random.uniform(10, 20)
    l.ChangeRatio = random.uniform(10, 20)
    l.TotalVolume = random.randint(100, 200)
    l.VWAP = random.randint(100, 200)
    l.CumulativeLowPrice = random.uniform(10, 20)
    l.CumulativeHighPrice = random.uniform(10, 20)
    l.CumulativeVWAP = random.randint(100, 200)
    return l


# 根据pid获取datetime对象
def pid2time(pid):
    td = datetime.today()
    if 1 <= pid <= 121:
        t = datetime(year=td.year, month=td.month, day=td.day, hour=9, minute=30, second=3)
        return t + timedelta(minutes=pid-1)
    elif 122 <= pid <= 241:
        t = datetime(year=td.year, month=td.month, day=td.day, hour=13, minute=1, second=3)
        return t + timedelta(minutes=pid-122)


# 构造一天的数据
def create_items():
    return [create_item(pid, pid2time(pid)) for pid in range(1, 242)]


def test_str():
    print(l2model_open(create_item(1, pid2time(1))))


# 测试 StatisticTask的 add函数
def test_add():
    t = StatisticTask(GSession)
    for item in create_items():
        t.add(item)
        t.add(item)
    print(t)
    return t

if __name__ == '__main__':
    # todo 学习和使用单元测试
    test_str()
    test_add()
