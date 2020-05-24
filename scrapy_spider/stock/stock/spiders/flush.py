# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from stock.items import StockItem
import time
import random

class FlushSpider(scrapy.Spider):
    name = 'flush'
    headers = {
            'Referer': 'http://quotes.money.163.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    #allowed_domains = []
    start_urls = ['http://www.iwencai.com/stockpick/search?ts=1&f=1&qs=stockhome_topbar_click&w=%E5%8F%A3%E7%BD%A9']


    def __init__(self):
        scrapy.Spider.__init__(self)
        self.stock_list = []
        with open('stock_file', 'r') as f:
            for l in f:
                self.stock_list.append(l[:-1])

    def start_requests(self):
        for stock_code in list(self.stock_list):
            self.curr_stock_code = str(stock_code)
            print stock_code
            url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(self.curr_stock_code)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        text = response.text
        soup = BeautifulSoup(text, 'lxml')
        print 'cur',self.curr_stock_code
        start_time = soup.find('input', {'name': 'date_start_type'}).get('value').replace('-','')
        end_time = soup.find('input', {'name':'date_end_type'}).get('value').replace('-', '')
        file_item = StockItem()
        if len(self.curr_stock_code) > 0:
            stock_code_a = str(self.curr_stock_code)
            if int(stock_code_a[0]) in (0,2,3,6,9):
                if int(stock_code_a[0]) in [6,9]:
                    new_stock_code = '0' + stock_code_a
                if int(stock_code_a[0]) in [0, 2, 3]:
                    if not int(stock_code_a[0:3]) in (201,202, 203, 204):
                        new_stock_code = '1' + stock_code_a
            download_url = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'.format(new_stock_code, start_time, end_time)
            file_item['file_urls'] = [download_url]
        yield file_item

