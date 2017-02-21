# coding:UTF-8
import logging
import time

from sqlalchemy import *
from sqlalchemy.dialects.mssql import INTEGER, VARCHAR, DECIMAL, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf.manager import *

log_path = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'log/'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename=log_path+'all.log',
                    filemode='a')
Base = declarative_base()


class OpenPriceModel(Base):
    __tablename__ = 'OpenPrice'
    SecurityID = Column(BIGINT, primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4), primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)  # 延时的秒数
    PRICE = Column(DECIMAL(precision=9, scale=3))  # (9,3)
    TDATE = Column(VARCHAR(length=30))

    def __str__(self):
        return '%s : %s, %s' % (self.SECCODE, self.MARKET, self.PID)


class TradePriceModel(Base):
    __tablename__ = 'TradePrice'
    SecurityID = Column(BIGINT, primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4), primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)  # 延时的秒数
    PRICE = Column(DECIMAL(precision=9, scale=3))  # (9,3)
    TDATE = Column(VARCHAR(length=30))

    def __str__(self):
        return '%s : %s, %s' % (self.SECCODE, self.MARKET, self.PID)


class OtherPriceModel(Base):
    __tablename__ = 'OtherPrice'
    SecurityID = Column(BIGINT, primary_key=True)
    PID = Column(INTEGER)
    MARKET = Column(VARCHAR(length=4), primary_key=True)
    SECCODE = Column(VARCHAR(length=6))
    SECNAME = Column(VARCHAR(length=20))
    DELAY = Column(INTEGER)  # 延时的秒数
    HIGH = Column(DECIMAL(precision=9, scale=3))  # (9,3)
    LOW = Column(DECIMAL(precision=9, scale=3))  # (9,3)
    SIGNAL = Column(DECIMAL(precision=9, scale=3))  # (9,3)
    TDATE = Column(VARCHAR(length=30))

    def __str__(self):
        return '%s : %s, %s' % (self.SECCODE, self.MARKET, self.PID)


def l2model_open(src):
    row_data = {
        'SecurityID': src.SecurityID,
        'SECCODE': src.Symbol,
        'PID': src.ProductID,
        'MARKET': src.Market,
        'SECNAME': src.ShortName.decode('UTF-8'),
        'PRICE': src.OpenPrice,
        'DELAY': int(time.time()) - int(src.UNIX / 1000),
        'TDATE': src.TradingDate
    }
    return OpenPriceModel(**row_data)


def l2model_trade(src):
    row_data = {
        'SecurityID': src.SecurityID,
        'SECCODE': src.Symbol,
        'PID': src.ProductID,
        'MARKET': src.Market,
        'SECNAME': src.ShortName.decode('UTF-8'),
        'PRICE': (src.HighPrice + src.LowPrice) / 20,
        'DELAY': int(time.time()) - int(src.UNIX / 1000),
        'TDATE': src.TradingDate
    }
    return TradePriceModel(**row_data)


def l2model_other(src):
    row_data = {
        'SecurityID': src.SecurityID,
        'SECCODE': src.Symbol,
        'PID': src.ProductID,
        'MARKET': src.Market,
        'SECNAME': src.ShortName.decode('UTF-8'),
        'HIGH': src.HighPrice,
        'LOW': src.LowPrice,
        'SIGNAL': (src.HighPrice + src.LowPrice) / 20,
        'DELAY': int(time.time()) - int(src.UNIX / 1000),
        'TDATE': src.TradingDate
    }
    return OtherPriceModel(**row_data)


def create_tables():
    Base.metadata.create_all(gengine)


def drop_tables():
    Base.metadata.drop_all(gengine)


# 根据json配置文件生成连接字符串
def load_conf_engine():
    con_str = '%s+%s://%s:%s@%s:%s/%s' % (
        gconf['dbms'], gconf['engine'], gconf['user'], gconf['pwd'],
        gconf['ip'], gconf['port'], gconf['dbname']
    )
    logging.debug('连接字符串为 :%s' % con_str)
    return create_engine(con_str)

# 全局唯一engine : global engine
gengine = load_conf_engine()
# 全局唯一Session类 : GSession
GSession = sessionmaker(bind=gengine)
