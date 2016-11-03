# coding:utf-8
from sqlalchemy import *
from sqlalchemy.dialects.mssql import INTEGER,VARCHAR,DATE,DATETIME,DECIMAL,NVARCHAR,BIGINT
import platform

class DBHelper:
    META = MetaData()
    DBNAME_FORMAT = 'GTA_SEL1_TRDMIN_%s'
    TBNAME_FORMAT = '%sL1_TRDMIN01_%s'
    REMOTE_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/%s'
    LOCAL_CONN = 'mssql+pymssql://admin:c0mm0n-adm1n@localhost/%s'
    CONN = REMOTE_CONN if platform.system() == 'Darwin' else LOCAL_CONN
    DBMAP,TBMAP = {},{}

    @staticmethod
    def dbName(month):
        return DBNAME_FORMAT % month

    @staticmethod
    def tbName(market,month):
        return TBNAME_FORMAT % (market,month)

    @staticmethod
    def getHisDB(month):
        '''返回进程安全的engine对象'''
        dbname = dbName(month)
        if dbname not in DBMAP:
            DBMAP[dbname] = create_engine(CONN % dbname,poolclass=NullPool)
        return DBMAP[dbname]

    @staticmethod
    def getTestDB():
        return create_engine('mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/TEST')

    @staticmethod
    def getHisTB(market,month):
        '''获取历史数据表的table对象'''
        dbname = dbname(month)
        tbname = tbName(market,month)
        if tbname not in TBMAP:
            t = Table(tbname,META,
                Column('SECCODE',NVARCHAR(length=6),primary_key=True),
                Column('SECNAME',NVARCHAR(length=20),primary_key=True),
                Column('TDATE',NVARCHAR(length=10),primary_key=True),
                Column('MINTIME',NVARCHAR(length=4),primary_key=True),
                Column('STARTPRC',DECIMAL(precision=9,scale=3)),
                Column('HIGHPRC',DECIMAL(precision=9,scale=3)),
                Column('LOWPRC',DECIMAL(precision=9,scale=3)),
                Column('ENDPRC',DECIMAL(precision=9,scale=3)),
                Column('MINTQ',DECIMAL(precision=12,scale=0)),
                Column('MINTM',DECIMAL(precision=18,scale=3)),
                Column('UNIX',BIGINT),
                Column('MARKET',NVARCHAR(length=4),primary_key=True)
            )
            t.create(DBMAP[dbname],checkfirst=True)
            TBMAP[tbname] = t
        return TBMAP[tbname]
