# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class A3987Tag(scrapy.Item):
    name = scrapy.Field()
    group = scrapy.Field()

class A3987Group(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    thumb = scrapy.Field()
    view_count = scrapy.Field()
    images = scrapy.Field()
    tags = scrapy.Field()
    cat = scrapy.Field()

#service=Picture.GetPictureList&plat=38&canal=wallpaper_xiaomi&id=159737&type=0&check=3f2eaf5d3ab1f9c6832c846ba4611673
class A3987Pic(scrapy.Item):
    group = scrapy.Field()
    image = scrapy.Field()

class A3987Error(scrapy.Item):
    url = scrapy.Field()



class JokeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    text = scrapy.Field()
    auth = scrapy.Field()
    auth_img = scrapy.Field()
    auth_url = scrapy.Field()


class WallpaperItem(scrapy.Item):
    thid = scrapy.Field()
    thumb = scrapy.Field()
    detail = scrapy.Field()
    dimens = scrapy.Field()
    mod_date = scrapy.Field()
    tags = scrapy.Field()


class S4399Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    text = scrapy.Field()
