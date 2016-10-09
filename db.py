# coding:UTF-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

engine = create_engine('mssql+pymssql://admin:c0mm0n-adm1n@202.115.75.13:3306/GTA_UPDATE')
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name,self.fullname,self.password)
