# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from s4399.items import WallpaperItem, JokeItem
import s4399.db.wallpaper as wall
import s4399.db.database as joke

class S4399Pipeline(object):
    def __init__(self):
        self.file = codecs.open('douban.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, JokeItem):
            dbItem = joke.dbJokeItem(item)
            joke.session.add(dbItem)
            joke.session.commit()
        elif isinstance(item, WallpaperItem):
            dbItem = wall.dbWallpaper(item)
            tag = wall.Tag(item)
            wall.session.merge(dbItem)
            wall.session.merge(tag)
            wall.session.commit()
        return item

    def spider_closed(self, spider):
        self.file.close()
