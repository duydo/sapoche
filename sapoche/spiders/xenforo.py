import scrapy

__author__ = 'duydo'

from scrapy.item import Item, Field


class AnyItem(Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value


class XenForoSpider(scrapy.Spider):
    def parse(self, response):
        for forum_url in response.css('.nodeTitle a::attr(href)').extract():
            forum_url = response.urljoin(forum_url)
            yield scrapy.Request(url=forum_url, callback=self.parse_forum_urls)

    def parse_forum_urls(self, response):
        link_group = response.css('.pageNavLinkGroup')
        if link_group:
            link_group = link_group[0]
            data_start = link_group.css('.PageNav::attr(data-start)').extract()
            data_last = link_group.css('.PageNav::attr(data-last)').extract()
            if data_start and data_last:
                for page in range(int(data_start[0]), int(data_last[0])):
                    page_url = '%spage-%s' % (response.url, page)
                    yield scrapy.Request(url=page_url, callback=self.parse_post_urls)
        self.parse_post_urls(response)

    def parse_post_urls(self, response):
        for post_url in response.css('.title a::attr(href)').extract():
            post_url = response.urljoin(post_url)
            yield scrapy.Request(url=post_url, callback=self.parse_posts)

    def parse_posts(self, response):
        for message in response.css('.messageList .message'):
            text = message.css('.messageText::text').extract()
            if text:
                print text[0].strip()
