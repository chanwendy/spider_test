# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pactencent.items import PactencentItem, PadtencentItem

class CtencentSpider(CrawlSpider):
    name = 'ctencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']
    front_url = 'http://hr.tencent.com/'

    rules = (
        # 在Rule中有restrict_xpath属性，restrict_xpath='xpath路径'，可以框定allow中re表达式的的选取范围。
        Rule(LinkExtractor(allow=r'start=.*?#a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'position_detail.php'), callback='parese_detail', follow=False),

    )

    def parse_item(self, response):
        node_list = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')
        item = PactencentItem()
        for i in node_list:
            item['position_name'] = i.xpath('//td/a/text()').extract_first()
            item['detail_url'] = self.front_url + i.xpath('//td/a/@href').extract_first()
            item['category'] = i.xpath('//td[2]/text()').extract_first()
            item['people_count'] = i.xpath('//td[3]/text()').extract_first()
            item['work_city'] = i.xpath('//td[4]/text()').extract_first()
            item['release_data'] = i.xpath('//td[5]/text()').extract_first()
            print(response.request.headers['User-Agent'])
            yield item


    def parese_detail(self, response):
        node_list = response.xpath('//ul[@class="squareli"]')
        item = PadtencentItem()
        item['job_duty'] = ''.join(node_list[0].xpath('//li/text()').extract())
        item['job_requirements'] = ''.join(node_list[1].xpath('//li/text()').extract())
        yield item

