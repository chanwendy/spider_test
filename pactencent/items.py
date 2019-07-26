# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PactencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position_name = scrapy.Field()
    category = scrapy.Field()
    people_count = scrapy.Field()
    work_city = scrapy.Field()
    release_data = scrapy.Field()
    detail_url = scrapy.Field()


class PadtencentItem(scrapy.Item):
    job_duty = scrapy.Field()
    job_requirements = scrapy.Field()
