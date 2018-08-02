# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShumassagescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    newsTitle = scrapy.Field()
    newsContent = scrapy.Field()
    newTime = scrapy.Field()
