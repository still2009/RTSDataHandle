import time,datetime
import os
import sched
import threading
import DSPStruct

msgTypeField = [4369, 12305, 12307, 12561]
nameField = ['BuyPrice01',
             'BuyPrice02',
             'BuyPrice03',
             'BuyPrice04',
             'BuyPrice05',
             'SellPrice01',
             'SellPrice02',
             'SellPrice03',
           'SellPrice04',
           'SellPrice05',
           'BuyVolume01',
           'BuyVolume02',
           'BuyVolume03',
           'BuyVolume04',
           'BuyVolume05',
           'SellVolume01',
           'SellVolume02',
           'SellVolume03',
           'SellVolume04',
           'SellVolume05']
msgTypeFieldT = [4368, 12560]
nameFieldT = ['Theta','Vega','Rho','Gamma']
msgTypeMap = {
    '4113':'上海证券交易所_分时数据_',
    '8209':'深圳证券交易所_分时数据_'
}

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
        pass

    def Save(self,msgType,data):
        conn = self.GetFileConn(msgType)
        conn.write(data + "\n")
        pass

    def GetFileConn(self, msgType):
        if msgType in self.__fileDic__:
            return self.__fileDic__.get(msgType)
        else:
            fileConn = open(self.StyleTime+"//"+str(msgType) + ".txt","a+")
            self.__fileDic__[msgType]= fileConn
            fileConn.write(self.GetFileHead(msgType)+"\n")
            return fileConn

    def Flush(self):
        for conn in self.__fileDic__.values():
            conn.flush()
        self.schedule.enter(self.inc, 0, self.Flush)

    def Close(self):
        for conn in self.__fileDic__.values():
            conn.flush()
            conn.close()

    def ScheduleStart(self):
        self.schedule.enter(self.inc, 0, self.Flush)
        self.schedule.run()
    # 添加ReceiveUNIX 和 receiveDate字段
    def GetFileHead(self, msgType):
        str1 = ""
        for ss in DSPStruct.__MsgTypeDic__.get(msgType)._fields_:
            if msgType in msgTypeField and ss[0] in nameField:
                continue
            if msgType in msgTypeFieldT and ss[0] in nameFieldT:
                continue
            if msgType == 4368 and ss[0] == 'Delta':
                continue
            if str1:
                str1 = str1 + "," +ss[0]
            else:
                str1 = ss[0]
        # 添加ReceiveUNIX字段
        str1 = str1 + ',' + 'ReceiveUNIX'
        # 添加ReceiveDate字段
        str1 = str1 + ',' + 'ReceiveDate'
        return str1



class SchFlush(threading.Thread):
    def __init__(self, ft):
        threading.Thread.__init__(self)
        self.fileutil = ft

    def run(self):
        self.fileutil.ScheduleStart()

if __name__ == "__main__":
    fileUtil = FileUtil()
    print("ssssssssssss")
    i = 0
    while(i<100):
        fileUtil.Save(12560,"xxxxxxxxxxxx")
        i = i+1
    fileUtil.Close()
