# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pactencent.items import PactencentItem, PadtencentItem

class PactencentPipeline(object):
    def open_spider(self, spider):
        self.file = open(r'brief.josn', 'w', encoding='UTF-8')

    def process_item(self, item, spider):
        if isinstance(item, PactencentItem):
            content = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class PadtencentPipeline(object):
    def open_spider(self, spider):
        self.file = open(r'detail.josn', 'w', encoding='UTF-8')

    def process_item(self, item, spider):
        if isinstance(item, PadtencentItem):
            content = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
