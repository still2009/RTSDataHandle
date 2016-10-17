#coding=utf-8
#这里需要引入三个模块
from update2db import *
import time, os, sched
from datetime import datetime
from datetime import timedelta
import sys

h,m,s=9,25,0
h2,m2,s2=15,5,0
if len(sys.argv) == 7:
    h,m,s,h2,m2,s2= int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),\
    int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
else:
    print('未输入定时参数,例如 9 25 0 15 10 0代表每天9点25分0s执行,15点10分0秒结束\n-->使用默认参数执行\n-->必须使用24小时制')

schedule = sched.scheduler(time.time, time.sleep)

def perform_begin():
    print('begin')
    begin()
    schedule.enter(getDelta(h2,m2,s2,False), 0, perform_end,())

def perform_end():
    print('end')
    end()
    schedule.enter(getDelta(h,m,s), 0, perform_begin,())

def timming_exe(delay):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(delay, 0, perform_begin,())
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()
def getDelta(h,m,s,tommorow=True):
    do = datetime.now()
    d = do
    if tommorow:
        d = do+timedelta(days=1)
    dd = datetime(year=d.year,month=d.month,day=d.day,hour=h,minute=m,second=s)
    delta = (dd-d).seconds
    print('当前时间-->%s\n执行时间-->%s\n即%s秒之后执行\n' % (do,dd,delta))
    return delta

if __name__ == '__main__':
    timming_exe(getDelta(h,m,s))
