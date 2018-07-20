# 启动文件
# from scrapy.cmdline import execute
#
# import sys
# import os
# # print(os.path.dirname(os.path.abspath(__file__)))
# # dirname父目录
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # 启动
# execute(["scrapy","crawl","douban_spider"])

from scrapy import cmdline
cmdline.execute('scrapy crawl douban_spider'.split())
