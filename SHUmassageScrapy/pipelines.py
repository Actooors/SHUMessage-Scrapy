# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from scrapy.crawler import Settings as settings
class ShumassagescrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def _init_(self):
        self.conn = pymysql.connect('118.25.130.89', 'root', '52655384', 'shumessage', charset='utf-8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = "insert into message_info(news_title, news_content, new_time) values (%s, %s,%d)"
        self.cursor.execute(insert_sql, (item["newsTitle"], item["newsContent"], item["newTime"]))
