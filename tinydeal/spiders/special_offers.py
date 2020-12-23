# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']


    def start_requests(self):
        yield scrapy.Request(url='https://www.tinydeal.com/specials.html' , callback=self.parse, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        })

    def parse(self, response):
        for item in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield{
                'item_name': item.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': response.urljoin(item.xpath(".//a[@class='p_box_title']/@href").get()),
                'price': item.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'discount': item.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath ("//a[@class='nextPage']/@href").get()

        yield scrapy.Request(url=next_page, callback=self.parse , headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        })
        