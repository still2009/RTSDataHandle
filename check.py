# coding:UTF-8

class DataCheck:
    '''
    该类负责数据检查数据中的异常，包含以下检测项：
    1. 空值
    2. 量比 = 现成交总手/(过去5日平均每分钟成交量 * 当日累计开市时间min)
    3. 涨幅 = (现价 - 上个交易日收盘价)/上个交易日收盘价 * 100%
    检查结果输出为日志文件,包含info,warning,error三种类型的信息
    '''
    def __init__(self):
        self.volumeRatio = 0
    
