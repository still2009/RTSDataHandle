# coding:UTF-8
import json
import time

from sqlalchemy import *
from sqlalchemy.dialects.mssql import INTEGER, VARCHAR, DECIMAL, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class OpenPriceModel(Base):
    __tablename__ = 'OpenPrice'
    SecurityID = Column(BIGINT,primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4),primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)# 延时的秒数
    PRICE = Column(DECIMAL(precision=9,scale=3))# (9,3)

class TradePriceModel(Base):
    __tablename__ = 'TradePrice'
    SecurityID = Column(BIGINT,primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4),primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)# 延时的秒数
    PRICE = Column(DECIMAL(precision=9,scale=3))# (9,3)

class OtherPriceModel(Base):
    __tablename__ = 'OtherPrice'
    SecurityID = Column(BIGINT,primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4),primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)# 延时的秒数
    HIGH = Column(DECIMAL(precision=9,scale=3))# (9,3)
    LOW = Column(DECIMAL(precision=9,scale=3))# (9,3)
    SIGNAL = Column(DECIMAL(precision=9,scale=3))# (9,3)

def L2OpenPrice(src):
    rowData = {}
    rowData['SecurityID'] = src.SecurityID
    rowData['SECCODE'] = src.Symbol
    rowData['PID'] = src.ProductID
    rowData['MARKET'] = src.Market
    rowData['SECNAME'] = src.ShortName.decode('UTF-8')
    rowData['PRICE'] = src.OpenPrice
    rowData['DELAY'] = int(time.time()) - int(src.UNIX/1000)
    return OpenPriceModel(**rowData)

def L2TradePrice(src):
    rowData = {}
    rowData['SecurityID'] = src.SecurityID
    rowData['SECCODE'] = src.Symbol
    rowData['PID'] = src.ProductID
    rowData['MARKET'] = src.Market
    rowData['SECNAME'] = src.ShortName.decode('UTF-8')
    rowData['PRICE'] = (src.HighPrice + src.LowPrice)/20
    rowData['DELAY'] = int(time.time()) - int(src.UNIX/1000)
    return TradePriceModel(**rowData)

def L2OtherPrice(src):
    rowData = {}
    rowData['SecurityID'] = src.SecurityID
    rowData['SECCODE'] = src.Symbol
    rowData['PID'] = src.ProductID
    rowData['MARKET'] = src.Market
    rowData['SECNAME'] = src.ShortName.decode('UTF-8')
    rowData['HIGH'] = src.HighPrice
    rowData['LOW'] = src.LowPrice
    rowData['SIGNAL'] = (src.HighPrice + src.LowPrice)/20
    rowData['DELAY'] = int(time.time()) - int(src.UNIX/1000)
    return OtherPriceModel(**rowData)


def createTables():
    Base.metadata.create_all(engine)

def dropTables():
    Base.metadata.drop_all(engine)

# 根据json配置文件生成连接字符串
def getConfEngine():
    conf = json.load(open('conf/db.conf', 'r'))
    constr = '%s+%s://%s:%s@%s:%s/%s' % (
    conf['dbms'], conf['engine'], conf['user'], conf['pwd'],
    conf['ip'], conf['port'], conf['dbname']
    )
    print('connection str is :\n%s\n' % constr)
    return create_engine(constr)

engine = getConfEngine()
Session = sessionmaker(bind=engine)
