# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from s4399.db.database import session, dbJokeItem

class S4399Pipeline(object):
    def __init__(self):
        self.file = codecs.open('douban.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        dbItem = dbJokeItem(item)
        session.add(dbItem)
        session.commit()
        return item

    def spider_closed(self, spider):
        self.file.close()
