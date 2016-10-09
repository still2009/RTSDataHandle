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
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SSEL1Min,DSPStruct.DT_SIXTY_MIN)

def getAllSZSEL1(conn,code):
    # 深圳证券交易所每1min股票数据
    conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_ONE_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIVE_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_TEN_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_FIFTEEN_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_THIRTY_MIN)
    conn.Subscribe(r'*',DSPStruct.EU_SZSEL1Min,DSPStruct.DT_SIXTY_MIN)
if __name__ == '__main__':
    conn = TDPS()
    with open('codes.csv','r') as codeFile:
        print('读取文件成功,订阅股票中...')
        for code in codeFile.readlines():
            getSSEL1(conn,code)
            getSZSEL1(conn,code)
        print('订阅完成')
    codeFile.close()
    print('关闭股票代码文件')
