# coding:UTF-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import VARCHAR,DATE,DATETIME,DECIMAL,NVARCHAR,BIGINT

Base = declarative_base()
class MinuteDataModel(Base):
    __tablename__ = 'MINUTE_DATA'
    DataID = Column(BIGINT,primary_key=True)
    SecurityID = Column(BIGINT)
    TradeTime = Column(DATETIME)
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

    def setTableName(tableName):
        self.__tablename__ = tableName

    def __repr__(self):
        return "<MinData(ShortName='%s', ProductID='%s', SecurityID='%s')>" % \
        (self.ShortName,self.ProductID,self.SecurityID)

def importFromCSV(fname,session):
    '''从csv文件导入数据'''
    with open(fname,'r') as f:
        # 第一行为表的字段
        fields = f.readline().split(',')
        # 其他行为数据
        for line in f.readlines():
            rowData = {}
            for key,value in zip(fields,line.split(',')):
                rowData[k] = value
            row = MinuteDataModel(**rowData)
            session.add(row)
        session.commit()

def createTable(engine):
    '''创建表格'''
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    engine = create_engine('mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13:1433/GTA_UPDATE')
    Session = sessionmaker(bind=engine)
    createTable(engine)
    print('succ')
    pass
