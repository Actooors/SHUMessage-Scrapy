# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
import json
import os
from scrapy.exporters import JsonItemExporter
import pymysql
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem

class ShumassagescrapyPipeline(object):
    def process_item(self, item, spider):
        # if item['create_date'] > datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'):
        return item

"""
    pipeline中只有MysqlTwistedPipeline在使用中
    异步导入数据库
    其他格式的pipeline只是拿来练手的
"""

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            password=settings["MYSQL_PASSWORD"],
            cursorclass=pymysql.cursors.DictCursor,
            database=settings["MYSQL_DBNAME"],
            charset='utf8',
            user=settings["MYSQL_USER"]
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 自定义的json导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("news.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 使用Jsonexporter
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open("newsexporter.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


project_dir = os.path.abspath(os.path.dirname(__file__))