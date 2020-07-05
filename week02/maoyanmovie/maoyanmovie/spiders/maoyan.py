# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from maoyanmovie.items import MaoyanmovieItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)


    # 解析函数
    def parse(self, response):
        # 打印网页的url
        # print(response.url)
        # 打印网页的内容
        # print(response.text)
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for index,movie in enumerate(movies):
            if index < 10:
                item = MaoyanmovieItem()
                name = movie.xpath('./a/text()').extract_first().strip()
                link = movie.xpath('./a/@href').extract_first().strip()
                item['name'] = name
                item['link'] = link
                link = f'https://maoyan.com{link}'
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    # 解析具体页面
    def parse2(self, response):
        item = response.meta['item']
        movie_details = Selector(response=response).xpath('//div[@class="movie-brief-container"]/ul/li[@class="ellipsis"]')
        item['show'] = movie_details[2].xpath('./text()').extract_first().strip()
        item_atags = []
        for atag in movie_details[0].xpath('./a'):
            show_text = atag.xpath('./text()').extract_first().strip()
            item_atags.append(show_text)
        item['movieType'] = '/'.join(item_atags)
        yield item