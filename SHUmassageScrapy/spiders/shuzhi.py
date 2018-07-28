# -*- coding: utf-8 -*-
import scrapy
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

    def parse(self, response):
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
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
