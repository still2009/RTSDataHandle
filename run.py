# coding:utf-8
# 负责项目部署
from dthandle.main import *
if __name__ == '__main__':
    globalConn = TDPS()
    # 监视线程,控制订阅和退订的周期性执行
    monitor = MonitorTask(start_receiver, (globalConn,), stop_receiver, (globalConn,))
    monitor.start()
