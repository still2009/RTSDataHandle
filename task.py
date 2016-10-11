# coding:UTF-8
from update2file import *
import time
from datetime import datetime

while True:
    print('开始计时')
    now = datetime.now()
    print(now)
    if now.hour == 8 and now.minute == 55:
        print('时间到达8:55，开始执行')
        update2file.begin()
        print('定时任务运行中,结束计时')
        break
    time.sleep(60)
