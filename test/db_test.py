# coding:utf-8
from db_process import *
from DSPStruct import Level1Min
from db import *
from datetime import datetime as dt
import time

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

DATA = '''60,204000002126,1476151500000,4294967295,b'000857',b'2016-10-11',b'2016-10-11 10:05:00.000',1476151500000,b'SSE',500医药,13255.13,13256.477,13255.13,13255.299,12285.0,25170952.0,13263.522,-0.812,-0.0001,662841,0.0,13233.555,13273.289,0.0,{},{}'''
DATA = DATA.format(time.time(),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
if sys.version_info.major == 2:
    DATA = DATA.decode('utf-8')
CONN = TEST_REMOTE_CONN if platform.system() == 'Darwin' else TEST_LOCAL_CONN
testEngine = create_engine(CONN)
TSession = sessionmaker(bind=testEngine)
createTable(testEngine)

finalThread = ConsumeThread('final',TSession,finalDelay=15,middleDelay=30)
middleThread = ConsumeThread('middle',TSession,finalDelay=15,middleDelay=30)
itemCounter = Counter()
itemCounter.start()
finalThread.start()
middleThread.start()


for i in range(10000):
    time.sleep(0.2)
    ss = 10 * (1 if i%2 == 0 else -1)
    DB_MinCallBack(Level1Min(Freq=i,UNIX=int((time.time()+ss)*1000)))
