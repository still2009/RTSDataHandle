import DSPStruct
from ctypes import *

__callBackDic__ = {}

def OnBaseConnectionState(ConnectCode):
    print ("ConnectCode:",ConnectCode)
	
pOnBaseConnectionStateFun = CFUNCTYPE(None, c_int)
pOnBaseConnectionStateHandle = pOnBaseConnectionStateFun(OnBaseConnectionState)

def OnBaseSubscribeMessage(msgType, pdata, nLen, errorCode, reqID):
    struct = DSPStruct.__MsgTypeDic__.get(msgType)
    if struct and reqID == 0 and errorCode == 0:
        data = struct.from_address(pdata)
        #if msgType in __callBackDic__  and data.ProductID != 4294967295:
        if msgType in __callBackDic__:
            __callBackDic__.get(msgType)(data)

pOnBaseSubscribeMessageFun = CFUNCTYPE(None, c_uint, c_ulonglong, c_int, c_int, c_uint)
pOnBaseSubscribeMessageHandle = pOnBaseSubscribeMessageFun(OnBaseSubscribeMessage)

def OnBaseRequestMessage(msgType, pdata, nLen, errorCode, reqID):
    struct = DSPStruct.__MsgTypeDic__.get(msgType)
    if struct and reqID == 0 and errorCode == 0:
        data = struct.from_address(pdata)
        if msgType in __callBackDic__:
            __callBackDic__.get(msgType)(data)

	
pOnBaseRequestMessageFun = CFUNCTYPE(None, c_uint, c_ulonglong, c_int, c_int, c_uint)
pOnBaseRequestMessageHandle = pOnBaseRequestMessageFun(OnBaseRequestMessage)


def regCallBack(msgType, callback):
    __callBackDic__[msgType] = callback
