import urllib2
import urllib
class Spider:
    def __init__(self):
        pass

    def parse(self, url):
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(req)
        print html.read()

if __name__ == "__main__":
    s = Spider()
    url = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%8F%A3%E7%BD%A9'
    #url  = 'http://www.baidu.com'
    s.parse(url)
