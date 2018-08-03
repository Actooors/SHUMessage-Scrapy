# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class ShumassagescrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def _init_