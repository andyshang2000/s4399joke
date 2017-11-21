# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from s4399.items import WallpaperItem, JokeItem, A3987Group, A3987Error
import s4399.db.wallpaper as wall
import s4399.db.wall3987 as w3987
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
        elif isinstance(item, A3987Error):
            e = w3987.Error()
            e.id = item['url']
            w3987.session.merge(e)
            w3987.session.commit()
        elif isinstance(item, A3987Group):
            g = w3987.Group()
            g.id = item['id']
            g.thumb = item['thumb']
            g.count = item['view_count']
            g.title = item['title']
            g.cat = item['cat']

            for tag in item['tags']:
                t = w3987.Tag()
                t.group = item['id']
                t.name = tag
                t.id = g.id + tag
                w3987.session.merge(t)

            c = 1
            for image in item['images']:
                img = w3987.Image()
                img.url = image
                img.group = item['id']
                img.id = item['id'] + "_" + str(c)
                c += 1
                w3987.session.merge(img)

            w3987.session.merge(g)
            w3987.session.commit()
        return item

    def spider_closed(self, spider):
        self.file.close()
