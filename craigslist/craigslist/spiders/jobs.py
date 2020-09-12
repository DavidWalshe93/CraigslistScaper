# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org/']
    start_urls = ['http://newyork.craigslist.org//']

    def parse(self, response):
        pass
