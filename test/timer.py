#coding=utf-8
#这里需要引入三个模块
from update2db import *
import time, os, sched
from datetime import datetime
# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)

def perform_command(cmd, inc):
    begin()
    schedule.enter(inc, 0, perform_command, (cmd, inc))

def timming_exe(cmd, inc = 3):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()


print("每日9:25开始抓取数据")
d = datetime.now()
dd = datetime(year=d.year,month=d.month,day=d.day,hour=9,minute=25)
delta = (dd-d).seconds
roundDelay =  3600*24
print('此次任务开始于 %s 即 %ss 后开始,周期为 %ss' % (dd,delta,roundDelay))
time.sleep(delta)
timming_exe("echo %time%", roundDelay)
