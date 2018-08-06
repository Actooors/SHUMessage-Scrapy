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

    def process_item(self, item, spider):
        conn = pymysql.connect(host='118.25.130.89', user='root', passwd='52655384', db='shumessage', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            "insert into message_info (news_title, news_content, new_time) values ('%s','%s','%s');"
            % (item["newsTitle"], item["newsContent"], item["newTime"])
        )
        conn.commit()
        cursor.close()  # 关闭游标
        conn.close()  # 释放数据库资源