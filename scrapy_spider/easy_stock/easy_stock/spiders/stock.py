# -*- coding: utf-8 -*-
import scrapy


class StockSpider(scrapy.Spider):
    name = 'stock'
    #allowed_domains = ['stock.com']
    
    def start_requests(self):
        urls = [
            'http://quote.eastmoney.com/center/gridlist.html#hs_a_board',
        ]
        headers = {
    	    'Referer': 'http://quote.eastmoney.com',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'        
        }
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)



    def parse(self, response):
        items = response.xpath('//*[@id="table_wrapper-table"]/tbody/tr')
        for item in items:
            stock_id = item.xpath('td[2]/a/text()').extract()[0]
            stock_name = item.xpath('td[3]/a/text()').extract()[0]
	    last_price = item.xpath('td[5]/span/text()').extract()[0]
	    increase_percent = item.xpath('td[6]/span/text()').extract()[0]
	    increase_amount = item.xpath('td[7]/span/text()').extract()[0]
	    turn_over_hand = item.xpath('td[8]/text()').extract()[0]
	    turn_over_amount = item.xpath('td[9]/text()').extract()[0]
	    amplitude = item.xpath('td[10]/text()').extract()[0]
	    highest = item.xpath('td[11]/span/text()').extract()[0]
	    lowest = item.xpath('td[12]/span/text()').extract()[0]
	    today_open = item.xpath('td[13]/span/text()').extract()[0]
	    yest_close = item.xpath('td[14]/text()').extract()[0]
	    quantity_relative_ratio = item.xpath('td[15]/text()').extract()[0]
	    turn_over_rate = item.xpath('td[15]/text()').extract()[0]
	    PE_ratio = item.xpath('td[16]/text()').extract()[0]
	    PB_ratio = item.xpath('td[17]/text()').extract()[0] 
        filename = 'stock_file'
        with open(filename, 'wb') as f:
            f.write(response.body)

