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
        """
        listings = response.xpath('//li[@class="result-row"]')

        for listing in listings:
            # Relative matching
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            url = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            title = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield scrapy.Request(url,
                                 callback=self.parse_listing,
                                 meta=dict(
                                     date=date,
                                     url=url,
                                     title=title
                                 ))

        # Move to the next page of data.
        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()
        if next_page_url:
            # url must be absolute.
            abs_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=abs_next_page_url, callback=self.parse)

    def parse_listing(self, response: scrapy.http.Response):
        """
        Parses an individual listing.
        """
        loader = ItemLoader(item=CraigslistItem(), response=response)

        date = response.meta["date"]
        url = response.meta["url"]
        title = response.meta["title"]

        compensation = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        job_type = response.xpath('//*[@class="attrgroup"]/span[2]/b/text()').extract_first()

        loader.add_value("date", date)
        loader.add_value("title", title)
        loader.add_value("url", url)
        loader.add_value("compensation", compensation)
        loader.add_value("job_type", job_type)

        yield loader.load_item()
