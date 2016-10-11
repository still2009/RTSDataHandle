# coding=UTF-8
from TDPS import *
from DSPStruct import *
import call

# 上海单支订阅
def getSSEL1(conn,code):
    # 上海证券交易所每1min股票数据
    conn.RegSSEL1MinCallBack(call.SSEL1MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(code,DSPStruct.EU_SSEL1Min,freq)
# 深圳单支订阅
def getSZSEL1(conn,code):
    # 深圳证券交易所每1min股票数据
    conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,freq)
# 上海全部订阅
def getAllSSEL1(conn):
    '''上海证券交易所分时数据'''
    conn.RegSSEL1MinCallBack(call.SSEL1MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,freq)
# 深圳全部订阅
def getAllSZSEL1(conn):
    '''深圳证券交易所分时数据'''
    conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
    for freq in (60,300,600,900,1800,3600):
        conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,freq)
def begin():
    conn = TDPS()
    print('连接成功')

    getAllSSEL1(conn)
    print('上海市场 分时数据订阅成功')

    getAllSZSEL1(conn)
    print('深圳市场 分时数据订阅成功')
if __name__ == '__main__':
    begin()
