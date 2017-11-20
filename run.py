# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
# @Author : woodenrobot
from scrapy import cmdline
import sys

name = 'bing_wallpaper'
if len(sys.argv) > 1:
    name = sys.argv[1]
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
