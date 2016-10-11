# coding:utf-8
import time,datetime
import os
import sched
import threading
import DSPStruct

msgTypeMap = {
    '4113':'上海证券交易所_分时数据_',
    '8209':'深圳证券交易所_分时数据_'
}
# add ReceiveDate
FIELDS = 'Freq,SecurityID,TradeTime,ProductID,Symbol,TradingDate,TradingTime,UNIX,Market,ShortName,OpenPrice,HighPrice,LowPrice,ClosePrice,Volume,Amount,BenchMarkOpenPrice,Change,ChangeRatio,TotalVolume,VWAP,CumulativeLowPrice,CumulativeHighPrice,CumulativeVWAP,ReceiveUNIX,ReceiveDate'

class FileUtil:
    def __init__(self):
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.inc = 30
        self.__fileDic__={}
        self.StyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        if not os.path.exists(self.StyleTime):
            os.mkdir(self.StyleTime)
        scf = SchFlush(self)
        scf.start()

    def Save(self,msgType,Freq,data):
        fname = '%s_%s' % (msgType,Freq)
        conn = self.GetFileConn(msgType,Freq)
        conn.write(data + "\n")

    def GetFileConn(self,msgType,Freq):
        fname = '%s_%s' % (msgType,Freq)
        if fname in self.__fileDic__:
            return self.__fileDic__.get(fname)
        else:
            fileConn = open(self.StyleTime+"//"+msgTypeMap[msgType] + str(Freq) + ".txt","a+")
            self.__fileDic__[fname]= fileConn
            fileConn.write(FIELDS+"\n")
            return fileConn

    def Flush(self):
        for conn in self.__fileDic__.values():
            conn.flush()
        # 延时30s执行
        self.schedule.enter(self.inc, 0, self.Flush)

    def Close(self):
        for conn in self.__fileDic__.values():
            conn.flush()
            conn.close()

    def ScheduleStart(self):
        self.schedule.enter(self.inc, 0, self.Flush)
        self.schedule.run()

class SchFlush(threading.Thread):
    def __init__(self, ft):
        threading.Thread.__init__(self)
        self.fileutil = ft

    def run(self):
        self.fileutil.ScheduleStart()

def test():
    fileUtil = FileUtil()
    data = 'test data xxxxxxxxxxxx'
    fileUtil.Save('4113',60,data)
    fileUtil.Save('4113',360,data)
    fileUtil.Save('4113',300,data)
    fileUtil.Save('8209',300,data)
if __name__ == "__main__":
    pass
