# coding=UTF-8
from TDPS import *
from DSPStruct import *
import call
import time

def getSSEL1(conn,code):
    # 上海证券交易所每1min股票数据
    conn.RegSSEL1MinCallBack(call.SSEL1MinCallBack)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(code,DSPStruct.EU_SSEL1Min,DSPStruct.DT_SIXTY_MIN)

def getSZSEL1(conn,code):
    # 深圳证券交易所每1min股票数据
    conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(code,DSPStruct.EU_SZSEL1Min,DSPStruct.DT_SIXTY_MIN)

def getAllSSEL1(conn):
    conn.RegSSEL1MinCallBack(call.SSEL1MinCallBack)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_SIXTY_MIN)

def getAllSZSEL1(conn):
    # 深圳证券交易所每1min股票数据
    conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(b'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_SIXTY_MIN)
def getAll(conn):
    with open('codes.csv','r') as codeFile:
        print('读取文件成功,拼接股票代码中...')
        code_str = ''.join(codeFile.readlines())
        print('订阅中')
        getSSEL1(conn,bytes(code_str,encoding='UTF-8'))
        getSZSEL1(conn,bytes(code_str,encoding='UTF-8'))
    codeFile.close()
    print('关闭股票代码文件')
if __name__ == '__main__':
    conn = TDPS()
    getAllSSEL1(conn)
    getAllSZSEL1(conn)
    # getAll(conn)
