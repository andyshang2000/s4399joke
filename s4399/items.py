# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JokeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    text = scrapy.Field()
    auth = scrapy.Field()
    auth_img = scrapy.Field()
    auth_url = scrapy.Field()


class S4399Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    text = scrapy.Field()
