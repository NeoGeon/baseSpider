# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline


class StockPipeline(object):
    def process_item(self, item, spider):
        return item
class SelfDefineFilePipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super(SelfDefineFilePipeline, self).__init__(*args, **kwargs)

    def file_path(self, request, response=None, info=None):
        str_temp = str(request.url)
        name = str_temp[54:61]
        name = name + '.csv'
        return name
