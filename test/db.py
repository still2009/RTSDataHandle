# coding:UTF-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import INTEGER,VARCHAR,DATE,DATETIME,DECIMAL,NVARCHAR,BIGINT
import time
from DSPStruct import Level1Min
import codecs
from file import FIELDS

Base = declarative_base()
REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13:1433/GTA_UPDATE'
LOCAL_CONN = 'mssql+pyodbc://admin:c0mm0n-adm1n@finx'
engine = create_engine(REMOTE_CONN)
Session = sessionmaker(bind=engine)

class MinuteDataModel(Base):
    __tablename__ = 'MINUTE_DATA'
    DataID = Column(BIGINT,primary_key=True)
    Freq = Column(INTEGER)
    SecurityID = Column(BIGINT)
    TradeTime = Column(BIGINT)
    ProductID = Column(BIGINT)
    Symbol = Column(VARCHAR(length=6,collation='Chinese_PRC_CI_AS'))# (6) COLLATE Chinese_PRC_CI_AS NOT NULL
    ShortName = Column(VARCHAR(length=20,collation='Chinese_PRC_CI_AS'))# (20) COLLATE Chinese_PRC_CI_AS NOT NULL
    TradingDate = Column(DATE)
    TradingTime = Column(DATETIME)
    UNIX = Column(BIGINT)
    Market = Column(NVARCHAR(length=4,collation='Chinese_PRC_CI_AS'))# (4) COLLATE Chinese_PRC_CI_AS NOT NULL
    OpenPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    HighPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    LowPrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
    ClosePrice = Column(DECIMAL(precision=9,scale=3))# (9,3)
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
    ReceiveUNIX = Column(DECIMAL(precision=12,scale=2))# 接收到数据时的本地实时间戳
    ReceiveDate = Column(DATETIME)# 接收到数据时的本地实时间

    def setTableName(tableName):
        self.__tablename__ = tableName

    def __repr__(self):
        return "<MinData(ShortName='%s', ProductID='%s', SecurityID='%s')>" % \
        (self.ShortName,self.ProductID,self.SecurityID)

# 将一行的字符串数据转换为ORM类对象
def Str2MinuteData(data):
    fields = FIELDS.split(',')

    fieldsType = [str(i[1]) for i in Level1Min._fields_]
    fieldsType.append('double')
    rowData = {}
    for key,value,ft in zip(fields,data.split(','),fieldsType):
        if value.startswith('b'): # 解析出b开头的数据
            value = value.split("'")[1]
        # 类型转换，从str到数字
        if ft.find('long') != -1:
            rowData[key] = int(value)
        elif ft.find('double') != -1:
            rowData[key] = float(value)
        else:
            print(value)
            rowData[key] = value
    print('begin consrtuct obj')
    return MinuteDataModel(**rowData)

def importFromCSV(fname,session):
    '''从csv文件导入数据'''
    with codecs.open(fname,'r','utf-8') as f:
        # 检查第一行是否为表的字段
        header = f.readline()
        if header.find('Freq') == -1:
            print('第一行不是字段列，按照默认顺序导入')
            session.add(Str2MinuteData(header))
        else:
            print('第一行是字段列,按照默认顺序到入,请检查是否一致')
        # 其他行为数据
        for line in f.readlines():
            row = Str2MinuteData(line)
            session.add(row)
        session.commit()

def createTable(engine):
    '''创建表格'''
    Base.metadata.create_all(engine)
def save(data,session):
    row = Str2MinuteData(data)
    session.add(row)
    session.commit()
if __name__ == '__main__':
    # createTable(engine)
    # importFromCSV('t.txt',Session())
    print('导入db模块成功')
    pass
