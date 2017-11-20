from sqlalchemy import Column, String, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from scrapy import log
import logging

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class dbJokeItem(Base):
    # 表的名字:
    __tablename__ = 'joke'

    # 表的结构:
    id = Column(String, primary_key=True)
    url = Column(String)
    image = Column(String)
    text = Column(String)
    auth = Column(String)
    auth_img = Column(String)
    auth_url = Column(String)

    def __init__(self, item):
        self.id = str(uuid4())
        self.url = self.getValue(item, 'url')
        self.image = self.getValue(item, 'image')
        self.text = self.getValue(item, 'text')
        self.auth = self.getValue(item, 'auth')
        self.auth_url = self.getValue(item, 'auth_url')
        self.auth_img = self.getValue(item, 'auth_img')

    def getValue(self, item, key):
        if key in item.keys():
            return item[key]
        return None


# 初始化数据库连接:
engine = create_engine('sqlite:///test3.db')
Base.metadata.create_all(engine)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
