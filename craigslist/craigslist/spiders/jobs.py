# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from craigslist.items import CraigslistItem


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/ofc/']

    def parse(self, response: scrapy.http.Response):
        """
        Parses content from a html page response.

        :param response: The page response/
        :return: The parsed payload.
        """
        listings = response.xpath('//li[@class="result-row"]')

        for listing in listings:
            loader = ItemLoader(item=CraigslistItem(), response=response)
            # Relative matching
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            url = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            title = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            loader.add_value("date", date)
            loader.add_value("title", title)
            loader.add_value("url", url)

            yield loader.load_item()

        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()

        if next_page_url:
            abs_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=abs_next_page_url, callback=self.parse)