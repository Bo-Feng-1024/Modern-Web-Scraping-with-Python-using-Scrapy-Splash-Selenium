# -*- coding: utf-8 -*-
from urllib.parse import uses_fragment
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc', headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]'), follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath('//div[@class="sc-94726ce4-2 khmuXj"]/h1/text()').get(),
            'year': response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"]/li[1]/span/text()').get(),
            'duration': response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"]/li[3]/text()').getall(),
            'genre': response.xpath('//li[@data-testid="storyline-genres"]/div/ul/li/a/text()').get(),
            'rating': response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]/text()').get(),
            'movie_url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }