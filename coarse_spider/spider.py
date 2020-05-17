# -*- coding: utf-8 -*-
import urllib2
import json
import csv
from urllib import quote


class Item:
    def __init__(self):
        self.allowed_fields = ("date", "newDead", "confirm", "heal", "newHeal", "dead", "newConfirm")
        self.data_field = {}

    def default_init(self):
        for field in self.allowed_fields:
            self.data_field[field] = -1

    def get_feed(self, _dict):
        for item in _dict:
            if item in self.allowed_fields :
                if item == 'date' and type(_dict[item]) != int:
                    self.data_field[item] = self.date_parse(_dict[item])
                else:
                    self.data_field[item] = int(_dict[item])
    
    def get(self, field):
        if field not in self.allowd_fields:
            return -1
        return self.data_field[field]

    def date_parse(self, date_str):
        yymmdd = 20200000 + int(date_str.split('.')[0])*100 + int(date_str.split('.')[1])
        return yymmdd


class CsvData:
    def __init__(self):
        self.items = []

    def append(self, item):
        self.items.append(item)

    def dump(self, file_name, fields):
        with open(file_name, 'w') as cs_f:
            writer = csv.DictWriter(cs_f, fields)
            writer.writeheader()
            new_order = sorted(self.items, key=lambda item : item.data_field['date'], reverse=False)
            for item in new_order:
                data_line = item.data_field
                writer.writerow(data_line)

class Spider:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.csvData = CsvData()

    def date_parse(self, date_str):
        yymmdd = 20200000 + int(date_str.split('.')[0])*100+int(date_str.split('.')[1])
        return yymmdd

    def parse(self, url):
        rsp = urllib2.urlopen(url)
        data = rsp.read()
        j = json.loads(data)
        cnt  = 0
        for js_item in j['data']:
            item = Item()
            item.get_feed(js_item)
            if item.data_field['date'] >= self.start and item.data_field['date'] < self.end:
                item = Item()
                item.get_feed(js_item)
                self.csvData.append(item)
                
    def dump(self):
        item = Item()
        fields = [f for f in item.allowed_fields]
        self.csvData.dump("hubei.csv", fields)


class NationSpider:

    def __init__(self, start, end, filename):
        self.start = start
        self.end = end
        self.csvData = CsvData() 
        self.filename = filename
        self.province = []
        self.total = {}

    def date_parse(self, date_str):
        yymmdd = 20200000 + int(date_str.split('.')[0])*100 + int(date_str.split('.')[1])
        return yymmdd

    def init_province(self):
        with open(self.filename) as f:
            for line in f:
                self.province.append(line[:-1])

    def parse(self, base_url):
        self.init_province()
        for province in self.province:
            s = Spider(self.start, self.end)
            url = base_url + quote(province)
            s.parse(url)
            print province
            for item in s.csvData.items:
                date = item.data_field["date"]
                if date not in self.total:
                    self.total[date] = {}
                    self.total[date]['date'] = date
                for field in item.data_field:
                    if field == 'date': continue
                    if field not in self.total[date]:
                        self.total[date][field] = 0
                    if item.data_field[field] >=0:
                        self.total[date][field] += item.data_field[field]
        for date in self.total:
            item = Item()
            item.get_feed(self.total[date])
            self.csvData.append(item)
        
    def dump(self):
        item = Item()
        fields = [f for f in item.allowed_fields]
        self.csvData.dump("quanguo.csv", fields)

if __name__ == "__main__":
    base_url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='
    url = base_url 
    ns = NationSpider(20200119, 20200514, "province")
    ns.parse(base_url)
    ns.dump()
    s = Spider(20200119, 20200514)
    s.parse('https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E6%B9%96%E5%8C%97')
    #print s.csvData.items[0].data_field
    s.dump()

