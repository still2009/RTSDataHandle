# coding:UTF-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import INTEGER,VARCHAR,DATE,DATETIME,DECIMAL,NVARCHAR,BIGINT
import sys,time,datetime
from DSPStruct import Level1Min
import codecs,platform,os,json

Base = declarative_base()
class MinuteDataModel(Base):
    '''
    实时分时数据表 MINUTE_DATA_TODAY 对应的类
    '''
    __tablename__ = 'MINUTE_DATA_TODAY'
    SecurityID = Column(BIGINT,primary_key=True)
    TDATE = Column(VARCHAR(length=10),primary_key=True)
    MINTIME = Column(VARCHAR(length=4),primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4),primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    UNIX = Column(BIGINT)
    DELAY = Column(INTEGER)# 延时的秒数
    STARTPRC = Column(DECIMAL(precision=9,scale=3))# (9,3)
    HIGHPRC = Column(DECIMAL(precision=9,scale=3))# (9,3)
    LOWPRC = Column(DECIMAL(precision=9,scale=3))# (9,3)
    ENDPRC = Column(DECIMAL(precision=9,scale=3))# (9,3)
    Volume = Column(DECIMAL(precision=12,scale=0))# (12,0)
    Amount = Column(DECIMAL(precision=18,scale=3))# (18,3)
    BenchMarkOpenPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    Change = Column(DECIMAL(precision=9,scale=3))# (9,3)
    ChangeRatio = Column(DECIMAL(precision=9,scale=4))# (9,4)
    TotalVolume = Column(BIGINT)#
    VWAP = Column(DECIMAL(precision=9,scale=3))# (9,3)
    CumulativeLowPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    CumulativeHighPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    CumulativeVWAP = Column(DECIMAL(precision=9,scale=3))# (9,3)

    def __repr__(self):
        return "<MinData(ShortName='%s', ProductID='%s', SecurityID='%s')>" % \
        (self.ShortName,self.ProductID,self.SecurityID)

# 将一行的字符串数据转换为ORM类对象
def Level1Min2MinuteData(src):
    rowData = {}
    rowData['SecurityID'] = src.SecurityID
    rowData['SECCODE'] = src.Symbol
    rowData['TDATE'] = src.TradingDate[:10]
    d = src.TradingTime
    rowData['MINTIME'] = d[11:13]+d[14:16]
    rowData['PID'] = src.ProductID
    rowData['UNIX'] = src.UNIX/1000
    rowData['MARKET'] = src.Market
    rowData['SECNAME'] = src.ShortName.decode('UTF-8')
    rowData['STARTPRC'] = src.OpenPrice
    rowData['HIGHPRC'] = src.HighPrice
    rowData['LOWPRC'] = src.LowPrice
    rowData['ENDPRC'] = src.ClosePrice
    rowData['Volume'] = src.Volume
    rowData['Amount'] = src.Amount
    rowData['BenchMarkOpenPrice'] = src.BenchMarkOpenPrice
    rowData['Change'] = src.Change
    rowData['ChangeRatio'] = src.ChangeRatio
    rowData['TotalVolume'] = src.TotalVolume
    rowData['VWAP'] = src.VWAP
    rowData['CumulativeLowPrice'] = src.CumulativeLowPrice
    rowData['CumulativeHighPrice'] = src.CumulativeHighPrice
    rowData['CumulativeVWAP'] = src.CumulativeVWAP
    rowData['DELAY'] = int(time.time()) - src.UNIX/1000
    return MinuteDataModel(**rowData)

def createTable():
    Base.metadata.create_all(engine)

# 根据json配置文件生成连接字符串
def getConfEngine():
    conf = json.load(open('db.conf','r'))
    constr = '%s+%s://%s:%s@%s:%s/%s' % (
    conf['dbms'],conf['engine'],conf['user'],conf['pwd'],
    conf['ip'],conf['port'],conf['dbname']
    )
    print('connection str is :\n%s\n' % constr)
    return create_engine(constr)

engine = getConfEngine()
Session = sessionmaker(bind=engine)
