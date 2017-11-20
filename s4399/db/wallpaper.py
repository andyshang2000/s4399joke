from sqlalchemy import Column, String, create_engine, MetaData
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
class Tag(Base):
    __tablename__ = 'tag'

    id = Column(String, primary_key=True)
    name = Column(String)
    pic = Column(String)

    def __init__(self, item):
        self.name = getValue(item, 'tags')
        self.pic = getValue(item, 'thid')
        self.id = self.name + self.pic

class dbWallpaper(Base):
    # 表的名字:
    __tablename__ = 'wallpaper'

    # 表的结构:
    id = Column(String, primary_key=True)
    thumb = Column(String)
    detail = Column(String)
    dimens = Column(String)
    mod_date = Column(String)
    tags = Column(String)

    def __init__(self, item):
        self.id = getValue(item, 'thid')
        self.thumb = getValue(item, 'thumb')
        self.detail = getValue(item, 'detail')
        self.dimens = getValue(item, 'dimens')
        self.mod_date = getValue(item, 'mod_date')
        self.tags = getValue(item, 'tags')



# 初始化数据库连接:
engine = create_engine('sqlite:///wallpaper.db')
Base.metadata.create_all(engine)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
