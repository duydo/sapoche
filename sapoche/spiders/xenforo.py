from scrapy import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

__author__ = 'duydo'

from scrapy.item import Item, Field


class AnyItem(Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value


class XenForoSpider(CrawlSpider):
    item = AnyItem

    rules = (
        Rule(LinkExtractor(allow=(r'forums/',)), follow=True),
        Rule(LinkExtractor(allow=(r'threads/',)), callback='parse_thread', follow=True),
    )

    fields = {
        'title': r'//*[@class="titleBar"]/h1//text()',
        'body': r'//*[@class="messageInfo primaryContent"]/div[@class="messageContent"]/article//text()'
    }

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': 'https://otosaigon.com'
        },
        'DOWNLOAD_DELAY': 15
    }

    def parse_thread(self, response):
        item = self.item()
        item['link'] = response.url
        for field, xpath in self.fields.iteritems():
            value = response.xpath(xpath).extract()
            item[field] = value
            self.logger.info(len(value))
        yield item
