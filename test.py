# coding=UTF-8
from TDPS import *
from DSPStruct import *
import call
import time

conn = TDPS()

conn.RegSSEL1QuoteCallBack(call.SSEL1QuoteCallBack)
conn.Subscribe(b"600256|600031",DSPStruct.EU_SSEL1Quote,DSPStruct.DT_Quote)
conn.unSubscribe(b"600031",DSPStruct.EU_SSEL1Quote,DSPStruct.DT_Quote)
#
#
# conn.RegSSEL1MinCallBack(call.SSEL1MinCallBack)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL1Min,DSPStruct.DT_ONE_MIN)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL1Min,DSPStruct.DT_FIVE_MIN)
#
#
# conn.RegSSEIOL1QuoteCallBack(call.SSEIOL1QuoteCallBack)
# conn.Subscribe(b"10000555|10000556",DSPStruct.EU_SSEIOL1Quote,DSPStruct.DT_Quote)
#
# conn.RegSSEIOL1MinCallBack(call.SSEIOL1MinCallBack)
# conn.Subscribe(b"10000555|10000556",DSPStruct.EU_SSEIOL1Min,DSPStruct.DT_ONE_MIN)
#
# conn.RegSSEIOL1StaticCallBack(call.SSEIOL1StaticCallBack)
# conn.Subscribe(b"10000555|10000556",DSPStruct.EU_SSEIOL1Static,DSPStruct.DT_Quote)
#
# conn.RegSSEL2AuctionCallBack(call.SSEL2AuctionCallBack)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL2Auction,DSPStruct.DT_Quote)
#
# conn.RegSSEL2IndexCallBack(call.SSEL2IndexCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SSEL2Index,DSPStruct.DT_Quote)
#
# conn.RegSSEL2OrderqueueCallBack(call.SSEL2OrderqueueCallBack)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL2Orderqueue,DSPStruct.DT_Quote)
#
# conn.RegSSEL2QuoteCallBack(call.SSEL2QuoteCallBack)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL2Quote,DSPStruct.DT_Quote)
#
# conn.RegSSEL2TransactionCallBack(call.SSEL2TransactionCallBack)
# conn.Subscribe(b"600256",DSPStruct.EU_SSEL2Transaction,DSPStruct.DT_Quote)
#
# conn.RegSZSEL1QuoteCallBack(call.SZSEL1QuoteCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL1Quote,DSPStruct.DT_Quote)
#
# conn.RegSZSEL1MinCallBack(call.SZSEL1MinCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL1Min,DSPStruct.DT_ONE_MIN)
#
# conn.RegSZSEL2IndexCallBack(call.SZSEL2IndexCallBack)
# conn.Subscribe(b"399001",DSPStruct.EU_SZSEL2Index,DSPStruct.DT_Quote)
#
# conn.RegSZSEL2OrderCallBack(call.SZSEL2OrderCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Order,DSPStruct.DT_Quote)
#
# conn.RegSZSEL2OrderqueueCallBack(call.SZSEL2OrderqueueCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Orderqueue,DSPStruct.DT_Quote)
#
#
# conn.RegSZSEL2QuoteCallBack(call.SZSEL2QuoteCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Quote,DSPStruct.DT_Quote)
#
# conn.RegSZSEL2StaticCallBack(call.SZSEL2StaticCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Static,DSPStruct.DT_Quote)
#
# conn.RegSZSEL2StatusCallBack(call.SZSEL2StatusCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Status,DSPStruct.DT_Quote)
#
#
# conn.RegSZSEL2TransactionCallBack(call.SZSEL2TransactionCallBack)
# conn.Subscribe(b"000001",DSPStruct.EU_SZSEL2Transaction,DSPStruct.DT_Quote)
#
# conn.RegCFFEXTFL2QuoteCallBack(call.CFFEXTFL2QuoteCallBack)
# conn.Subscribe(b"TF1609",DSPStruct.EU_CFFEXTFL2Quote,DSPStruct.DT_Quote)
#
#
# conn.RegCFFEXTFL2MinCallBack(call.CFFEXTFL2MinCallBack)
# conn.Subscribe(b"TF1609",DSPStruct.EU_CFFEXTFL2Min,DSPStruct.DT_ONE_MIN)
#
# conn.RegCFFEXFFL2QuoteCallBack(call.CFFEXFFL2QuoteCallBack)
# conn.Subscribe(b"IF1612",DSPStruct.EU_CFFEXFFL2Quote,DSPStruct.DT_Quote)
#
#
# conn.RegCFFEXFFL2MinCallBack(call.CFFEXFFL2MinCallBack)
# conn.Subscribe(b"IF1612",DSPStruct.EU_CFFEXFFL2Min,DSPStruct.DT_ONE_MIN)
#
# conn.RegCFFEXIOL2QuoteCallBack(call.CFFEXIOL2QuoteCallBack)
# conn.Subscribe(b"HO1610-C-2000",DSPStruct.EU_CFFEXIOL2Quote,DSPStruct.DT_Quote)
#
#
# conn.RegCFFEXIOL2MinCallBack(call.CFFEXIOL2MinCallBack)
# conn.Subscribe(b"HO1610-C-2000",DSPStruct.EU_CFFEXIOL2Min,DSPStruct.DT_ONE_MIN)
#
#
# conn.RegSHFEL1QuoteCallBack(call.SHFEL1QuoteCallBack)
# #conn.Subscribe(b"AL1707",DSPStruct.EU_SHFEL1Quote,DSPStruct.DT_Quote)
# conn.Subscribe(b"*",DSPStruct.EU_SHFEL1Quote,DSPStruct.DT_Quote)
#
#
# conn.RegSHFEL1MinCallBack(call.SHFEL1MinCallBack)
# #conn.Subscribe(b"AL1707",DSPStruct.EU_SHFEL1Min,DSPStruct.DT_ONE_MIN)
# conn.Subscribe(b"*",DSPStruct.EU_SHFEL1Min,DSPStruct.DT_ONE_MIN)
#
#
# conn.RegDCEL1QuoteCallBack(call.DCEL1QuoteCallBack)
# #conn.Subscribe(b"BB1707",DSPStruct.EU_DCEL1Quote,DSPStruct.DT_Quote)
# conn.Subscribe(b"*",DSPStruct.EU_DCEL1Quote,DSPStruct.DT_Quote)
#
# conn.RegDCEL1MinCallBack(call.DCEL1MinCallBack)
# #conn.Subscribe(b"BB1707",DSPStruct.EU_DCEL1Min,DSPStruct.DT_ONE_MIN)
# conn.Subscribe(b"*",DSPStruct.EU_DCEL1Min,DSPStruct.DT_ONE_MIN)
#
#
# conn.RegDCEL1ArbitrageCallBack(call.DCEL1ArbitrageCallBack)
# #conn.Subscribe(b"BB1707",DSPStruct.EU_DCEL1Arbitrage,DSPStruct.DT_Quote)
# conn.Subscribe(b"*",DSPStruct.EU_DCEL1Arbitrage,DSPStruct.DT_Quote)
#
#
# conn.RegCZCEL1QuoteCallBack(call.CZCEL1QuoteCallBack)
# #conn.Subscribe(b"FG1707",DSPStruct.EU_CZCEL1Quote,DSPStruct.DT_Quote)
# conn.Subscribe(b"*",DSPStruct.EU_CZCEL1Quote,DSPStruct.DT_Quote)
#
# conn.RegCZCEL1MinCallBack(call.CZCEL1MinCallBack)
# conn.Subscribe(b"*",DSPStruct.EU_CZCEL1Min,DSPStruct.DT_ONE_MIN)
#
# time.sleep(10)
# conn.unSubscribe(b"600256",DSPStruct.EU_SSEL1Quote,DSPStruct.DT_Quote)
