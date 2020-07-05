# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import pymysql

class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        sql ="INSERT INTO `top10` (`name`, `movieType`,`show`) VALUES (%s, %s, %s)"
        values = (item['name'],item['movieType'],item['show'])
        # windows需要使用gbk字符集
        conn = pymysql.connect(host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'password',
            database = 'movie',
            charset = 'utf8mb4'
        )
        try:
            # 获得cursor游标对象
            cur = conn.cursor()
            cur.execute(sql, values)
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()
        return item
