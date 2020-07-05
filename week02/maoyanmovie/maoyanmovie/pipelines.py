# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        # name = item['name']
        # show = item['show']
        # movieType = item['movieType']
        # output = f'|{name}|\t|{show}|\t|{movieType}|'
        # with open('./doubanmovie.cvs', 'a+', encoding='utf-8') as article:
        #     article.write(output)
        item_list = [[item['name'], item['movieType'], item['show']]]
        movie = pd.DataFrame(data = item_list)
        # windows需要使用gbk字符集
        movie.to_csv('./movie.csv', mode='a+', encoding='utf8', index=False, header=False)
        return item
