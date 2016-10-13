# coding:utf-8
from db import *
DATA = '''60,204000002126,1476151500000,4294967295,b'000857',b'2016-10-11',b'2016-10-11 10:05:00.000',1476151500000,b'SSE',500医药,13255.13,13256.477,13255.13,13255.299,12285.0,25170952.0,13263.522,-0.812,-0.0001,662841,0.0,13233.555,13273.289,0.0,{},{}'''
DATA = DATA.format(time.time(),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
if sys.version_info.major == 2:
    DATA = DATA.decode('utf-8')
CONN = TEST_REMOTE_CONN if platform.system() == 'Darwin' else TEST_LOCAL_CONN
testEngine = create_engine(CONN)
TSession = sessionmaker(bind=testEngine)
createTable(testEngine)
save(DATA,TSession())
