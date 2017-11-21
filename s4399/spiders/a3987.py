# -*- coding: utf-8 -*-
import scrapy
import json
import s4399.items as items

id_list = ['3437',
           '3366',
           '3368',
           '3372',
           '3367',
           '3371',
           '3606',
           '3370',
           '3373',
           '3374',
           '3376',
           '3377',
           '3378',
           '3369',
           '3380',
           '3379',
           '3537',
           '3430']


class A3987Spider(scrapy.Spider):
    name = '3987'
    start_urls = ['http://s.3987.com/']
    handle_httpstatus_list = [400, 403, 502]

    config = None
    page = 1
    cat_index = 0
    # id = '3365'
    id = id_list[cat_index]
    url = 'http://s.3987.com/api-2.1/Public/demo/index.php'

    def start_requests(self):
        self.readStatus()
        self.id = id_list[self.cat_index]
        # service = Picture.GetHeadTag & plat = 38 & canal = wallpaper_xiaomi & check = 522395c85f2a3aa796ba31b704a22f3a
        # service = Picture.GetHeadBanner & plat = 38 & canal = wallpaper_xiaomi & check = c24cb1d6fabc48c43a4f16044e5caa7b
        # service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3365&page=1&pageSize=30&check=0471298247ed590cd69582d90ea392ff
        # service=Tag.ChangeTag&plat=38&canal=wallpaper_xiaomi&pageSize=24&check=6ab717047869ff715fa80dfda9a6e368
        # service=Search.GetPicture&plat=38&canal=wallpaper_xiaomi&title=%E6%AD%8C%E6%89%8B&page=1&pageSize=24&type=1&check=0702431b6b5d3db9fcd19a133d4f9652
        # FormRequest 是Scrapy发送POST请求的方法
        # yield scrapy.FormRequest(
        #     url=url,
        #     # Picture.GetRecommend
        #     formdata={"service": 'Picture.GetChoice',
        #               "plat": '38',
        #               "canal": 'wallpaper_xiaomi',
        #               "page": '1',
        #               "pageSize": '24',
        #               "check": '439e6524fa56ad9dbe7a4d8314f23a1f'},
        #     callback=self.parse
        # )
        yield scrapy.FormRequest(
            url=self.url,
            # Picture.GetRecommend
            formdata={"service": 'Picture.GetWallpaperList',
                      "plat": '38',
                      "canal": 'wallpaper_xiaomi',
                      "id": self.id,
                      "page": str(self.page),
                      "pageSize": '24',
                      "check": '2dd7fe5a5b0a664b72b46691d26a8989'},
            callback=self.parse
        )

    def readStatus(self):
        try:
            self.config = open('.config', 'r')
            obj = json.load(self.config)
        except Exception as err:
            obj = {"cat_index": self.cat_index, "page": self.page}
            self.writeStatus()
        try:
            self.config.close()
        except Exception as err:
            pass
        self.cat_index = obj['cat_index']
        self.page = obj['page']



    def writeStatus(self):
        self.config = open('.config', 'w')
        json.dump({"cat_index": self.cat_index, "page": self.page}, self.config)
        self.config.close()

    def parse(self, response):
        body = response.body.decode('utf-8')
        try:
            obj = json.loads(str(body))
        except Exception as err:
            print(str(body))
            return;
        self.writeStatus()
        if 'info' not in obj['data'] or len(obj['data']['info']) < 24:
            self.cat_index += 1
            self.id = id_list[self.cat_index]
            self.page = 1
        else:
            infolist = obj['data']['info']
            for obj in infolist:
                group = items.A3987Group()
                group['id'] = obj['id']
                group['title'] = obj['title']
                group['thumb'] = obj['thumb']
                group['view_count'] = obj['count']

                yield scrapy.FormRequest(
                    url=self.url,
                    # Picture.GetRecommend
                    formdata={"service": 'Picture.GetPictureList',
                              "plat": '38',
                              "canal": 'wallpaper_xiaomi',
                              "id": obj['id'],
                              "type": '2',
                              "check": '2dd7fe5a5b0a664b72b46691d26a8989'},
                    meta={'group': group,
                          # "proxy":'http://127.0.0.1:808'
                          },
                    callback=self.parsePicList
                )

            self.page += 1
        yield scrapy.FormRequest(
            url=self.url,
            # Picture.GetRecommend
            formdata={"service": 'Picture.GetWallpaperList',
                      "plat": '38',
                      "canal": 'wallpaper_xiaomi',
                      "id": self.id,
                      "page": str(self.page),
                      "pageSize": '24',
                      "check": '2dd7fe5a5b0a664b72b46691d26a8989'},
            # meta={"proxy":'http://127.0.0.1:808'},
            callback=self.parse
        )

    def parsePicList(self, response):
        group = response.meta['group']
        body = response.body.decode('utf-8')
        try:
            obj = json.loads(str(body))
            data = obj['data']['info']['data']
            group['images'] = data['imageurl']
            group['tags'] = data['tags'].split(',')
            group['cat'] = self.id
            yield group
        except Exception as err:
            errItem = items.A3987Error
            errItem.url = response.request.body
            yield errItem


'''
美女 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3365&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
性感 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3437&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
帅哥 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3366&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
游戏 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3368&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
动漫 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3372&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
明星 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3367&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
动物 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3371&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
卡通 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3606&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
汽车 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3370&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
影视 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3373&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
体育 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3374&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
城市 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3376&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
风景 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3377&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
唯美 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3378&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
创意 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3369&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
植物 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3380&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
日历 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3379&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
节日 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3537&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
其他 service=Picture.GetWallpaperList&plat=38&canal=wallpaper_xiaomi&id=3430&page=1&pageSize=30&check=4ba78072ab6c8eed323fbba8793f36d9
'''
