# coding:UTF-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import INTEGER,VARCHAR,DATE,DATETIME,DECIMAL,NVARCHAR,BIGINT
import time,datetime
from DSPStruct import Level1Min
import codecs,platform
from file import FIELDS

Base = declarative_base()
REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13:1433/GTA_UPDATE'
TEST_REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13:1433/TEST'
TEST_LOCAL_CONN = 'mssql+pyodbc://admin:c0mm0n-adm1n@finx_test'
LOCAL_CONN = 'mssql+pyodbc://admin:c0mm0n-adm1n@finx'
CONN = REMOTE_CONN if platform.system() == 'Darwin' else LOCAL_CONN
engine = create_engine(CONN)

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
    fieldsType.append('double')# receive_unix
    fieldsType.append('xxx')# ReceiveDate
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
            rowData[key] = value
    print(rowData)
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
def getSession():
    return Session()
def save(data,session):
    row = Str2MinuteData(data)
    session.add(row)
    session.commit()
def test():
    DATA = '''60,204000002126,1476151500000,4294967295,b'000857',b'2016-10-11',b'2016-10-11 10:05:00.000',1476151500000,b'SSE',500医药,13255.13,13256.477,13255.13,13255.299,12285.0,25170952.0,13263.522,-0.812,-0.0001,662841,0.0,13233.555,13273.289,0.0,{},{}'''
    DATA = DATA.format(time.time(),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    DATA = DATA.decode('utf-8')
    CONN = TEST_REMOTE_CONN if platform.system() == 'Darwin' else TEST_LOCAL_CONN
    engine = create_engine(CONN)
    testEngine = create_engine(CONN)
    TSession = sessionmaker(bind=testEngine)
    createTable(testEngine)
    save(DATA,TSession())
if __name__ == '__main__':
    # importFromCSV('t.txt',Session())
    # test()
    print('导入db模块成功')
    pass
