# coding:utf-8
from sqlalchemy import *
from sqlalchemy.pool import NullPool
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

    @classmethod
    def dbName(cls,month):
        return cls.DBNAME_FORMAT % month

    @classmethod
    def tbName(cls,market,month):
        return cls.TBNAME_FORMAT % (market,month)

    @classmethod
    def getHisDB(cls,month):
        '''返回进程安全的engine对象'''
        dbname = cls.dbName(month)
        if dbname not in cls.DBMAP:
            cls.DBMAP[dbname] = create_engine(cls.CONN % dbname,poolclass=NullPool)
        return cls.DBMAP[dbname]

    @staticmethod
    def getTestDB():
        return create_engine('mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13/TEST')

    @classmethod
    def getHisTB(cls,market,month):
        '''获取历史数据表的table对象'''
        dbname = cls.dbName(month)
        tbname = cls.tbName(market,month)
        if tbname not in cls.TBMAP:
            t = Table(tbname,cls.META,
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
            t.create(cls.getHisDB(dbname),checkfirst=True)
            cls.TBMAP[tbname] = t
        return cls.TBMAP[tbname]
DBHelper.getHisDB('201010')
DBHelper.getHisTB('SH','201212')
