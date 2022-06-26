# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksScrapeSpider(CrawlSpider):
    name = 'books_scrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[@class="product_pod"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]'), follow=True)
    )

    def parse_item(self, response):
        yield {
            'book_name': response.xpath('//h1/text()').get(),
            'price': response.xpath('//p[@class="price_color"]/text()').get(),
        }
