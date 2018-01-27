# -*- coding: utf-8 -*-
import scrapy


class BzspiderSpider(scrapy.Spider):
    name = 'bzspider'

    def parse(self, response):
        pass
import scrapy
import datetime
import time

from Newspider.items import SnapshotItem
from Newspider.items import ArticleItem
from scrapy.http import Request


class BzspiderSpider(scrapy.Spider):
    #
    name = 'bzspider'
    allowed_domains = ['www.bz-berlin.de']
    start_urls = ['http://www.bz-berlin.de/']
    
    def start_request(self,respponse):
        #
        urls = ['http://www.bz-berlin.de/']
        for url in urls:
            yield scrapy.Request(url=url,callback=parse,errback = errback_httpbin,dont_filter=True)
    
    def parse(self,response):
        #
        page = SnapshotItem()
        page['url'] = response.url       
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        page['timestamp'] = st
        ranks= []
        sections = response.css('div[class="row"]')
        for idx,block in enumerate(sections):
            articles = block.xpath('.//div/div')
            for idy,article in enumerate(articles):
                href = article.xpath('a/@href').extract_first()
                #request = scrapy.Request(url=href,callback = self.parse_article)
                if(href):
                    article = ArticleItem()
                    article['url'] = href
                    yield article
                    #filter article 
                    ranks.append(href)
        page['rank'] = ';\n'.join(ranks)        
        yield page

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)