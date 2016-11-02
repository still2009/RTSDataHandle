# coding:utf-8
from db import *
import os,multiprocessing,codecs
from progressbar import *

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
    读取单个csv文件，并将每一行数据转换为model对象
    要求单个csv文件内只出现一个月的数据,全文月份唯一
    返回：
        resMap : month-rows的map
    '''
    rows = []
    f = codecs.open(fname,'r','utf-8')
    for line in f.readlines():
        if line.startswith('#'):
            continue
        else:
            rows.append(formatConvert(line))
    return {rows[0].TDATE[:-2]:rows}

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

def processDB():
    '''
    处理数据库相关的事务
    根据数据的日期信息决定commit到的数据库和表
    '''
    results = processCsvDir('./test')
    months = []
    for i in results:
        for k in i:
            months.append(k)
    months = set(tuple(months))
    LOCAL_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/%s'
    engineMap = {}
    tableMap = {}
    SessionMap = {}
    for i in months:
        engineMap[i] = create_engine(LOCAL_CONN % (dbNameHis % i))
        SessionMap[i] = sessionmaker(bind=engineMap[i])
        for market in ('SSE','SZSE'):
            tableMap[i][market] = createHisTable(tbNameHis % (market,i))
    for i in results:
        for k in i:
            session = SessionMap[k]()
            session.add_all(i[k])
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError,e:
                print('插入的数值重复导致异常(不满足逐渐约束)')
                continue
def intoDB(csvDir='./test'):
    # 进度条
    widgets = ['当前rows:',Percentage(),Bar(),' ',SimpleProgress()]
    bar = ProgressBar(widgets = widgets,maxval=1000).start()

    results = processCsvDir(csvDir)
    REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/%s'
    LOCAL_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@localhost/%s'
    CONN = REMOTE_CONN if platform.system() == 'Darwin' else LOCAL_CONN
    print('CONN is %s' % CONN)
    engine = create_engine(CONN % (dbNameHis % '201212'))
    HistoryDataModel.__table__.create(engine,checkfirst=True)
    Session = sessionmaker(bind=engine)
    for i in bar(range(len(results))):
        res = results[i]
        for k in res:
            session = Session()
            session.add_all(res[k])
            try:
                session.commit()
            except:
                print('出现commit异常，主键约束触发，继续')
                continue
            session.close()
def test():
    print os.getcwd()
    r = processCsvDir(os.path.join(os.getcwd(),'test'))
    print len(r)
    for i in r:
        for k in i:
            print('%s - %s' % (k,len(i[k])))
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('使用默认csv路径，非测试环境下禁止使用！,请务必指定目录')
        intoDB()
    else:
        intoDB(sys.argv[1])
