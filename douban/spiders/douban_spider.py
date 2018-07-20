# -*- coding: utf-8 -*-
# 爬取豆瓣TOP250电影
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url，扔到调度器里面，再由引擎丢到解析器里面，也就是parse函数
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法，这里是返回数据的解析
    def parse(self, response):
        # 循环电影的条目，比如第一页25条数据
        movies_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for i_item in movies_list:
            # item文件导进来
            doubanitem = DoubanItem()
            # 详细的数据的解析
            doubanitem["rank_num"] = i_item.xpath('.//div[@class="item"]//em/text()').extract_first()
            doubanitem["title"] = i_item.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span[1]/text()').extract_first()
            content = i_item.xpath('.//div/div[2]/div[2]/p[1]/text()').extract()
            # 数据的处理
            for i_content in content:
                content_s = "".join(i_content.split())
                doubanitem["introduce"] = content_s

            doubanitem["star"] = i_item.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[2]/text()').extract_first()
            doubanitem["comments"] = i_item.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').extract_first()
            doubanitem["describe"] = i_item.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            # print(doubanitem)
            # 需要将数据yield到pipeline（管道）去，后续可进行数据的存储，清洗，去重
            yield doubanitem
            # 获取下一页的条目
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        # 如果取得到
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
