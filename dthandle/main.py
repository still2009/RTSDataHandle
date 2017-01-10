# coding=UTF-8
import math
from datetime import datetime as dt

from TDPS import *

from dthandle.tasks import *

# 复用的全局线程变量
itemCounter = None  # 带打印的计数器线程
task = None  # 数据统计线程


# 订阅回调函数，接收到数据是被调用，应该在该函数中处理接收到的数据。
def db_callback(l):
    global itemCounter, task
    # 先丢弃修正数据(mintime在当前时间之前)
    now = dt.now()
    hour = int(l.TradingTime[11:13])
    minute = int(l.TradingTime[14:16])
    # 丢弃修正数据
    if hour < now.hour or (hour == now.hour and minute < now.minute):
        return
    # 使用ProductID过滤中间数据,使用SecurityID过滤股票
    if math.floor(l.SecurityID / 1000000000) == 201 and l.ProductID != 4294967295:
        itemCounter.step()
        task.add(l)


# 上海单支订阅
def sub_sh(conn, code):
    # 上海证券交易所所有频率的股票数据
    conn.RegSSEL1MinCallBack(db_callback)
    for freq in (60, 300, 600, 900, 1800, 3600):
        conn.Subscribe(code, DSPStruct.EU_SSEL1Min, freq)


# 深圳单支订阅
def sub_sz(conn, code):
    # 深圳证券交易所所有频率的股票数据
    conn.RegSZSEL1MinCallBack(db_callback)
    for freq in (60, 300, 600, 900, 1800, 3600):
        conn.Subscribe(code, DSPStruct.EU_SZSEL1Min, freq)


# 综合数据订阅函数
def sub_all(conn, code=b'*', freq=-1, market='A'):
    freqs = [freq] if freq != -1 else [60, 300, 600, 900, 1800, 3600]
    if market == 'A' or market == 'SH':
        for freq in freqs:
            conn.RegSSEL1MinCallBack(db_callback)  # 上海回调注册
            conn.Subscribe(code, DSPStruct.EU_SSEL1Min, freq)
        logging.info('上海订阅成功')
    if market == 'A' or market == 'SZ':
        for freq in freqs:
            conn.RegSZSEL1MinCallBack(db_callback)  # 深圳回调注册
            conn.Subscribe(code, DSPStruct.EU_SZSEL1Min, freq)
        logging.info('深圳订阅成功')


# 综合数据退订函数
def unsub_all(conn):
    conn.RegSSEL1MinCallBack(db_callback)
    conn.RegSZSEL1MinCallBack(db_callback)
    for freq in (60, 300, 600, 900, 1800, 3600):
        conn.unSubscribe(b'*', DSPStruct.EU_SZSEL1Min, freq)
    logging.info('退订成功')


# 启动接收器
def start_receiver(conn, f=60):
    # 初始化2个线程
    global itemCounter, task
    itemCounter = Counter()
    task = StatisticTask(GSession)
    # 先删除表再创建,目的是清空数据
    logging.info('删除表')
    drop_tables()
    logging.info('创建表')
    create_tables()
    logging.info('启动子线程...')
    itemCounter.start()
    task.start()
    logging.info('开始订阅')
    sub_all(conn, freq=f)


# 停止接收器
def stop_receiver(conn):
    unsub_all(conn)
    logging.info('关闭子线程')
    global itemCounter, task
    if itemCounter is not None:
        itemCounter.stop()
        logging.info('计数器子线程关闭成功')
    if task is not None:
        task.stop()
        logging.info('统计器子线程关闭成功')


if __name__ == '__main__':
    pass
