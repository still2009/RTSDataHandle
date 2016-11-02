# coding:utf-8
from db import *
import os,multiprocessing,codecs

dbNameHis = 'GTA_SEL1_TRDMIN_%s'
tbNameHis = '%sL1_TRDMIN01_%s'

def formatConvert(dataStr):
    '''
    将国泰安HBASE数据获取客户端数据获取程序
    获得的SEL1数据逗号分隔的字符串转换成HistoryDataModel对象
    并设置正确的表名称

    此函数要求传入数据的格式正确
    '''
    fields = dataStr.split(',')
    l = len(fields)
    if l < 11:
        print('csv行切分后列数为%s,异常返回' % l)
        return None
    s_m = fields[0].split('.')

    # 根据market和month 指定ORM类和表的映射
    rowObj = HistoryDataModel()
    rowObj.SECCODE = s_m[0]
    rowObj.SECNAME = fields[2]
    rowObj.TDATE = fields[3]
    rowObj.MINTIME = fields[4]
    rowObj.STARTPRC = float(fields[5])
    rowObj.HIGHPRC = float(fields[6])
    rowObj.LOWPRC = float(fields[7])
    rowObj.ENDPRC = float(fields[8])
    rowObj.MINTQ = float(fields[9]) # Volume成交手
    rowObj.MINTM = float(fields[10]) # Amount成交量
    rowObj.UNIX = int(fields[11])
    rowObj.MARKET = s_m[1]
    return rowObj

def processCsv(fname):
    '''
    读取单个csv文件，并将每一行数据转换为model对象并commit到数据库
    要求单个csv文件内只出现一个月的数据,全文月份唯一
    返回：
        true
    '''
    REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/%s'
    LOCAL_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@localhost/%s'
    CONN = REMOTE_CONN if platform.system() == 'Darwin' else LOCAL_CONN
    print('CONN is %s' % CONN)
    engine = create_engine(CONN % (dbNameHis % '201212'))
    HistoryDataModel.__table__.create(engine,checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    f = codecs.open(fname,'r','utf-8')
    print('导入%s中..' % fname)
    for line in f.readlines():
        if line.find('#') != -1:
            continue
        else:
            obj = formatConvert(line)
            if obj != None:
                session.add(obj)
                if len(session.new) == 5000:
                    session.commit()
    session.commit()
    session.close()
    print('导入%s结束..' % fname)
    return True

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
    print('csv文件个数 : %s' % len(fileList))
    results = pool.map(processCsv,fileList)
    return results

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('请务必指定csv文件的目录')
        exit(0)
    else:
        processCsvDir(sys.argv[1])
