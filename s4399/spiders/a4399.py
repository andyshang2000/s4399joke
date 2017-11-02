# -*- coding: utf-8 -*-
import scrapy
from s4399.items import JokeItem
from bs4 import BeautifulSoup


class A4399Spider(scrapy.Spider):
    name = '4399'
    allowed_domains = ['4399.com', '4399pk.com']
    start_urls = ['http://joke.4399pk.com/dryhumor/list-p-1.html']

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        div = soup.find('div', attrs={'class': 'pages'})
        for a in div.findAll('a'):
            if a.string == '下一页':
                yield response.follow(a.attrs['href'], self.parse)

        div_list = soup.findAll('div', attrs={'class': 'content'})
        for div in div_list:
            a = div.find('a')
            yield response.follow(a.attrs['href'], self.parseContent)

    def parseContent(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        div = soup.find('div', attrs={'class': 'jokewp'})
        authdiv = div.find('div', attrs={'class': 'author'})
        autha = authdiv.find('a')
        auth_img = autha.find('img')
        content = div.find('div', attrs={'id': 'dryhumor-content'})
        content_img = content.find('img')
        item = JokeItem()
        item['url'] = response.url
        if content_img is not None:
            item['image'] = content_img.attrs['src']
        item['text'] = content.text
        item['auth'] = autha.text
        if auth_img is not None:
            item['auth_img'] = auth_img.attrs['src']
            item['auth_img'] = item['auth_img'].replace('small', 'middle')
        item['auth_url'] = autha.attrs['href']
        yield item
