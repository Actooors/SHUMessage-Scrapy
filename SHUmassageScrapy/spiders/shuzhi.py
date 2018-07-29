# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
import json

class ShuzhiSpider(scrapy.Spider):
    name = 'shuzhi'
    allowed_domains = ['www.sz.shu.edu.cn']
    start_urls = ['http://www.sz.shu.edu.cn/']
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        "Host": "www.sz.shu.edu.cn",
        "Referer": "http://www.sz.shu.edu.cn/Login.aspx?ReturnUrl=http://www.sz.shu.edu.cn/index.aspx",
        "User-Agent": agent
    }
    session = requests.session()

    # def get_total_url(self, response):
    #     """
    #     提取出通知公告页面更多项的url
    #     """
    #     Total_urls = response.css(".MoreList a::attr(href)").extract()  #获取通知公告栏url
    #     News_urls = str(response.url) + Total_urls[0]
    #     yield scrapy.Request(News_urls, headers=self.header, callback=self.get_sort_url)
    #
    # def get_sort_url(self, response):
    #     """
    #     提取出各个边栏的url以便获取具体新闻的url
    #     """
    #     urls = response.css(".Gonggaotag li a::attr(href)").extract()
    #     Sorts_url = []
    #     for url in urls:
    #         Sorts_url.append("http://sz.shu.edu.cn"+url)
    #     for Sort_url in Sorts_url:
    #         yield scrapy.Request(Sort_url, headers=self.header, callback=self.get_news_url)

    def get_news_url(self, response):
        """
        使用深度优先的方法，首先提取出所有的新闻url再进一步进行内容提取
        """
        news_url = response.css(".Tongzhiul a::attr(href)").extract()
        urls = []
        for new_url in news_url:
            if not new_url.startswith("http"):
                url = "http://sz.shu.edu.cn"+new_url
                urls.append(url)
            else:
                urls.append(new_url)
        pass

    def parse_detail(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('http://www.sz.shu.edu.cn/Login.aspx', headers=self.header, callback=self.login)]

    def login(self,response):
        #熟知网模拟登录实现
        post_url = "http://www.sz.shu.edu.cn/api/Sys/Users/Login"
        post_data = {
            "username": "16121666",
            "password": "Xw52655384"
        }
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "message" in text_json and text_json["message"] == "成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header,callback=self.get_news_url)
