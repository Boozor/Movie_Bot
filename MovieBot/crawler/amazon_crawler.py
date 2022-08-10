
# -*- coding: cp1251 -*-
from __future__ import unicode_literals

import re
import codecs

import html2text
import scrapy
import ujson
from scrapy.http import Request, HtmlResponse
from middleware import RotateUserAgentMiddleware
from bs4 import BeautifulSoup

class RiaSpider(scrapy.Spider):

    domain = 'https://www.amazon.com'
    name = domain

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'COOKIES_ENABLED': True,
        'EXTENSIONS': {
            'scrapy.telnet.TelnetConsole': None,
        },
        'LOG_LEVEL': 'INFO',
        'LOG_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 20,
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'DOWNLOAD_DELAY': 0.25,

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'middleware.RotateUserAgentMiddleware': 400
        },

    }

    amazon = ujson.load(open('amazon2.json'))
    print(amazon.keys())
    start_urls = []
    for k in amazon.keys():
        start_urls.append('https://www.amazon.com/product-reviews/' + k)

    start = 0

    def start_requests(self):
        start = self.start + 1
        for start_url in self.start_urls:
            date = start_url[30:40]
            print(start_url)
            i = self.start_urls.index(start_url)
            yield Request(start_url,
                          dont_filter=False,
                          callback=self.parse_news_page,
                          meta={'date': date, 'i': i})

    def parse_news_page(self, response):
        event_title = response.css('title ::text').extract()

        event_data = {
            'event_title': event_title,
            'event_url': response.url,
        }

        yield event_data
