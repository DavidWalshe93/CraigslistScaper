# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from craigslist.items import CraigslistItem


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org/']
    start_urls = ['http://newyork.craigslist.org/search/egr']

    def parse(self, response):
        """
        Parses content from a html page response.

        :param response: The page response/
        :return: The parsed payload.
        """
        # loader = ItemLoader(item=JobsSpider(), response=response)

        listing = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        urls = response.xpath('//a[@class="result-title hdrlnk"]/@href').extract()

        for listing, url in zip(listing, urls):
            yield dict(
                listing=listing,
                url=url
            )

        # loader.add_value("title", title)
        # loader.add_value("url", url)
        #
        # return loader.load_item()


