# -*- coding: utf-8 -*-
import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div"): 

            yield {
                'product_name': product.xpath("normalize-space(.//div[@class='p-title']/a/text())").get(),
                'product_url': product.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                'product_img_url': product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@src").get(),
                'product_price': product.xpath(".//div[@class='p-price']//span/text()").get()
            }
        
        next_page = response.xpath("//ul[@class='pagination']/li[position() = last()]/a/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
