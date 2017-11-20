# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from s4399.items import WallpaperItem
from urllib import parse


class BingWallpaperSpider(scrapy.Spider):
    name = 'bing_wallpaper'
    keywords = ['风景手机壁纸', '自然手机壁纸', '动漫手机壁纸', '建筑手机壁纸', '美女手机壁纸', '二次元手机壁纸', '搞笑手机壁纸', '游戏手机壁纸', '炫酷手机壁纸', '好看手机壁纸',
                '美少女手机壁纸', '魔法手机壁纸', '非主流手机壁纸', '卡通手机壁纸', '儿童手机壁纸', '旅游手机壁纸',
                '最新手机壁纸', '色调手机壁纸', '暖色手机壁纸', '萌萌哒手机壁纸', 'EXO手机壁纸', '明星手机壁纸',
                '女神手机壁纸', '清新手机壁纸', '唯美手机壁纸', '纯色手机壁纸', '健身手机壁纸', '提醒手机壁纸',
                '老年人手机壁纸', '汽车手机壁纸', '飞机手机壁纸', '蓝色手机壁纸', '视觉系手机壁纸', '个性手机壁纸',
                '影视手机壁纸', '熊出没手机壁纸', '屌丝手机壁纸', '电脑手机壁纸', '互联网手机壁纸', '天气手机壁纸']
    keyword = '普朗克手机壁纸'
    first = 2
    count = 20
    # allowed_domains = ['']
    url = 'https://cn.bing.com/images/async?q=' + keyword + '&first=' + str(first) + '&count=' + str(
        count) + '&qft=+filterui%3aaspect-tall+filterui%3aimagesize-large&mmasync=1'
    start_urls = [url]

    thidlist = []

    def next_page(self):
        self.first += self.count
        return 'https://cn.bing.com/images/async?q=' + self.keyword + '&first=' + str(self.first) + '&count=' + str(
            self.count) + '&qft=+filterui%3aaspect-tall+filterui%3aimagesize-large&mmasync=1'

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        div = soup.find('div', attrs={'class': 'imgpt'})
        hit = False
        divcount = 0
        while div is not None:
            dimens = div.text
            a = div.find_next('a')
            detail_href = a.attrs['href']
            img = a.find_next('img')
            thumb = img.attrs['src']
            item = WallpaperItem()
            item['thumb'] = thumb
            item['dimens'] = dimens
            item['tags'] = self.keyword
            # yield response.follow('http://m.bai.c)
            div = div.find_next('div', attrs={'class': 'imgpt'})
            obj = parse.urlparse('https://cn.bing.com' + detail_href)
            dic = parse.parse_qs(obj.query)
            item['thid'] = dic['thid'][0]
            del dic['q']
            del dic['simid']
            del dic['selectedIndex']
            del dic['qft']
            for k in dic:
                dic[k] = dic[k][0]
            new_query = parse.urlencode(dic)
            new_url = obj.scheme + "://" + obj.netloc + obj.path + '?' + new_query

            divcount += 1
            yield response.follow(new_url, self.parseDetails,
                                  meta={'item': item, 'thid': dic['thid'], 'url': new_url})
        if divcount == self.count:
            yield response.follow(self.next_page(), self.parse)
        else:
            self.first = 2
            self.keyword = self.keywords.pop()
            yield response.follow(self.next_page(), self.parse)

    def parseDetails(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        item = response.meta['item']
        imgs = soup.find_all('img')

        hit = False
        img = soup.find('img', attrs={'class': 'mainImage'})
        if img is not None:
            a = img.find_parent('a')
            if a is not None:
                item['detail'] = a.attrs['href']
                hit = True
            elif 'src2' in img.attrs:
                item['detail'] = img.attrs['src2']
                hit = True
        else:
            for img in imgs:
                url = img.attrs['src']
                obj = parse.urlparse(url)
                dic = parse.parse_qs(obj.query)
                if 'id' in dic and dic['id'] == response.meta['thid']:
                    print(url)
                    a = img.find_parent('a')
                    item['detail'] = a.attrs['href']
                    hit = True
        if not hit:
            ref_url = response.meta['url']
            print(ref_url)
            print(response.meta['thid'])
        yield item
