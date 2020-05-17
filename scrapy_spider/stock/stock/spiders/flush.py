# -*- coding: utf-8 -*-
import scrapy


class FlushSpider(scrapy.Spider):
    name = 'flush'
    headers = {
            'Referer': '',
            'User-Agent:'}
    #allowed_domains = []
    start_urls = ['http://www.iwencai.com/stockpick/search?ts=1&f=1&qs=stockhome_topbar_click&w=%E5%8F%A3%E7%BD%A9']

    def start_requests(self):
        for stock code in list(self.stock_lost):
            self.curr_stock_code = str(stock_code.get('stock_id'))
            url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(self.curr_stock_code)
            yield scrapy.Request(url=url, header=self.headers, callback=self.parse)

    def parse(self, response):
        text = response.text
        soup = bs(text, 'lxml')
        start_time = soup.find('input', {'name': 'date_start_type'}).get('value').replace('-','')
        end_time = soup.find('input', {'name':'date_end_type'}).get('value').replace('-', '')
        time.sleep(random.choice([1,2]))

        file_time = StockItem()
        if len(self.current_stock_code) > 0:
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

