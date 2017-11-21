from sqlalchemy import Column, String, create_engine, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from scrapy import log
import logging

# 创建对象的基类:
Base = declarative_base()


def getValue(item, key):
    if key in item.keys():
        return item[key]
    return None

# 定义User对象:
class Image(Base):
    __tablename__ = 'image'
    id = Column(String, primary_key=True)
    url = Column(String)
    group = Column(String)

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(String, primary_key=True)
    name = Column(String)
    group = Column(String)

class Error(Base):
    __tablename__ = "err"

    id = Column(String, primary_key=True)

class Group(Base):
    # 表的名字:
    __tablename__ = 'group'

    # 表的结构:
    id = Column(String, primary_key=True)
    thumb = Column(String)
    title = Column(String)
    count = Column(String)
    cat = Column(String)



# 初始化数据库连接:
engine = create_engine('sqlite:///w3987.db')
Base.metadata.create_all(engine)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
