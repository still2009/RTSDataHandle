#coding=utf-8
#这里需要引入三个模块
from update2db import *
import time, os, sched
from datetime import datetime
import sys
if len(sys.argv) != 5:
    print('请输入定时参数,例如 9 25 30 1 代表每天9点25分30s执行，周期为1s')
    exit(0)
h,m,s,r = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
schedule = sched.scheduler(time.time, time.sleep)

def perform_command(cmd, inc):
    begin()
    # print('haha')
    schedule.enter(inc, 0, perform_command, (cmd, inc))

def timming_exe(cmd, inc = 3):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()


print("每日9:25开始抓取数据")
d = datetime.now()
dd = datetime(year=d.year,month=d.month,day=d.day,hour=h,minute=m,second=s)
delta = (dd-d).seconds
roundDelay =  r
print('此次任务开始于 %s 即 %ss 后开始,周期为 %ss' % (dd,delta,roundDelay))
time.sleep(delta)
timming_exe("echo %time%", roundDelay)
