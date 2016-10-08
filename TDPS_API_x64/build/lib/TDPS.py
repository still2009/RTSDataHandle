# coding=UTF-8
from ctypes import *
import DSPStruct
import os
import Callback
from distutils.sysconfig import get_python_lib

_TimeOut_ = 30

class TDPS:
    def __init__(self):
        self._TDPS_API_ = "libTDPSApi64.dll"
        import ctypes
        #load TDPS module
        self.api = ctypes.CDLL(self._TDPS_API_)
        self.Init()
        self.Start()

    def Init(self):
        #when first start system, init Tdps interface
        self.api.TDpscip_Init()

        #set callback function
        self.api.TDpscip_RegConnectionCB(Callback.pOnBaseConnectionStateHandle)
        self.api.TDpscip_RegSubscribeCB(Callback.pOnBaseSubscribeMessageHandle)
        self.api.TDpscip_RegRequestCB(Callback.pOnBaseRequestMessageHandle)

    def Start(self):
        self.api.TDpscip_Start()

    def Subscribe(self, Symbol, MsgType, DataFreq, nTimeOut = _TimeOut_):
        if MsgType not in Callback.__callBackDic__:
            print ("error:MsgType "+str(MsgType)+ " callback method not register")
            return
        
        subitem = DSPStruct.UserSubItem()
        subitem.vecQuoteCollection = Symbol
        subitem.tagDataFreq = DataFreq
        subitem.StMsgType = MsgType
        subitem.nTimeOut = nTimeOut

        requestID = c_ushort(0)

        self.api.TDpscip_Subscribe.restype = c_int
        self.api.TDpscip_Subscribe.argtypes = (POINTER(DSPStruct.UserSubItem), c_int)
        
        res = self.api.TDpscip_Subscribe(byref(subitem), 10, byref(requestID))
        print("Subscribe Result:"+str(res))

    def unSubscribe(self, Symbol, MsgType, DataFreq):
        subitem = DSPStruct.UserSubItem()
        subitem.vecQuoteCollection = Symbol
        subitem.tagDataFreq = DataFreq
        subitem.StMsgType = MsgType
        subitem.nTimeOut = _TimeOut_

        requestID = c_ushort(0)

        self.api.TDpscip_Subscribe.restype = c_int
        self.api.TDpscip_Subscribe.argtypes = (POINTER(DSPStruct.UserSubItem), c_int)
        
        res = self.api.TDpscip_Subscribe(byref(subitem), 11, byref(requestID))
        print("Subscribe Result:"+ str(res))

    #Request
    def Request(self, Symbol, MsgType, DataFreq, StartTime, EndTime, nTimeOut = _TimeOut_):
        if MsgType not in Callback.__callBackDic__:
            print ("error:MsgType "+str(MsgType) + " callback method not register")
            return
        
        reqitem = DSPStruct.UserRequestItem()
        reqitem.vecQuoteCollection = Symbol
        reqitem.tagDataFreq = DataFreq
        reqitem.StMsgType = MsgType
        reqitem.strStartTime = StartTime
        reqitem.strEndTime = EndTime
        reqitem.nTimeOut = nTimeOut

        requestID = c_ushort(0)
        self.api.TDpscip_Subscribe.restype = c_int
        res=self.api.TDpscip_Request(byref(reqitem), byref(requestID))
        print("Request Result:"+ str(res))


    def RegSSEL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL1Quote, callback)
        pass

    def RegSSEL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL1Min, callback)
        pass

    def RegSSEIOL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEIOL1Quote, callback)
        pass

    def RegSSEIOL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEIOL1Min, callback)
        pass

    def RegSSEIOL1StaticCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEIOL1Static, callback)
        pass

    def RegSSEL2AuctionCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL2Auction, callback)
        pass
    
    def RegSSEL2IndexCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL2Index, callback)
        pass

    def RegSSEL2OrderqueueCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL2Orderqueue, callback)
        pass

    def RegSSEL2QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL2Quote, callback)
        pass

    def RegSSEL2TransactionCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SSEL2Transaction, callback)
        pass

    def RegSZSEL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL1Quote, callback)
        pass

    def RegSZSEL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL1Min, callback)
        pass

    def RegSZSEL2IndexCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Index, callback)
        pass

    def RegSZSEL2OrderCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Order, callback)
        pass

    def RegSZSEL2OrderqueueCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Orderqueue, callback)
        pass
    
    def RegSZSEL2QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Quote, callback)
        pass

    def RegSZSEL2StaticCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Static, callback)
        pass

    def RegSZSEL2StatusCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Status, callback)
        pass

    def RegSZSEL2TransactionCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SZSEL2Transaction, callback)
        pass

    def RegCFFEXTFL2QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXTFL2Quote, callback)
        pass

    def RegCFFEXTFL2MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXTFL2Min, callback)
        pass

    def RegCFFEXFFL2QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXFFL2Quote, callback)
        pass

    def RegCFFEXFFL2MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXFFL2Min, callback)
        pass

    def RegCFFEXIOL2QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXIOL2Quote, callback)
        pass

    def RegCFFEXIOL2MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CFFEXIOL2Min, callback)
        pass

    def RegSHFEL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SHFEL1Quote, callback)
        pass

    def RegSHFEL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_SHFEL1Min, callback)
        pass

    def RegDCEL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_DCEL1Quote, callback)
        pass

    def RegDCEL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_DCEL1Min, callback)
        pass

    def RegDCEL1ArbitrageCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_DCEL1Arbitrage, callback)
        pass

    def RegCZCEL1QuoteCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CZCEL1Quote, callback)
        pass

    def RegCZCEL1MinCallBack(self, callback):
        Callback.regCallBack(DSPStruct.EU_CZCEL1Min, callback)
        pass

    #Stop
    def Stop(self):
        self.api.TDpscip_Stop()


if __name__ == '__main__':
    conn = TDPS();
    #Request(b"600256", DSPStruct.EU_SSEL1Min, DSPStruct.DT_ONE_MIN, b"20160809092000",b"20160809093000")
    conn.Subscribe(b"600256", DSPStruct.EU_SSEL1Min, DSPStruct.DT_ONE_MIN)
    
