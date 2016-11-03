# coding:utf-8
import sys,os,multiprocessing,codecs
import logging
from DBHelper import *

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')
dbNameHis = 'GTA_SEL1_TRDMIN_%s'
tbNameHis = '%sL1_TRDMIN01_%s'

def dataParse(dataStr):
    fields = dataStr.split(',')
    l = len(fields)
    if l < 11:
        logging.info('csv行切分后列数为%s,异常返回' % l)
        return None
    s_m = fields[0].split('.')

    # 根据market和month
    rowMap = {}
    rowMap['SECCODE'] = s_m[0]
    rowMap['SECNAME'] = fields[2]
    rowMap['TDATE'] = fields[3]
    rowMap['MINTIME'] = fields[4]
    rowMap['STARTPRC'] = float(fields[5])
    rowMap['HIGHPRC'] = float(fields[6])
    rowMap['LOWPRC'] = float(fields[7])
    rowMap['ENDPRC'] = float(fields[8])
    rowMap['MINTQ'] = float(fields[9]) # Volume成交手
    rowMap['MINTM'] = float(fields[10]) # Amount成交量
    rowMap['UNIX'] = int(fields[11])
    rowMap['MARKET'] = s_m[1]
    return rowMap

def processCsv(fname):
    '''
    读取单个csv文件，并将每一行数据转换为model对象并commit到数据库
    要求单个csv文件内只出现一个月的数据,全文月份唯一
    返回：
        true
    '''
    rows,errCount,count = [],0,0
    logging.info('导入%s中..' % fname)
    eg = DBHelper.getHisDB('201212')
    # eg = DBHelper.getTestDB()
    # HistoryDataModel.__table__.create(eg,checkfirst=True)
    for line in codecs.open(fname,'r','utf-8'):
        if line.find('#') != -1:
            continue
        obj = dataParse(line)
        if obj != None:
            count += 1
            try:
                eg.execute(HistoryDataModel.__table__.insert(),rows)
            except Exception as e:
                errCount += 1
    logging.info('导入%s结束,count->errCount = (%s,%s)' % (fname,count,errCount))
    return True if errCount == 0 else False

def processCsvDir(csvPath):
    '''
    处理所有的csv文件
    '''
    fileList = []
    # 将csv所在的目录下所有的.csv文件添加到队列
    for f in os.listdir(csvPath):
        absPath = os.path.join(csvPath,f)
        if os.path.isfile(absPath) and absPath.endswith('.csv'):
            fileList.append(absPath)
    # 进程池
    pool = multiprocessing.Pool(10)
    logging.info('csv文件个数 : %s' % len(fileList))
    results = pool.map(processCsv,fileList)
    for i,j in zip(results,fileList):
        logging.info('%s-%s' % (j,i))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        logging.info('请务必指定csv文件的目录')
        # processCsvDir('.')
        exit(0)
    else:
        processCsvDir(sys.argv[1])
