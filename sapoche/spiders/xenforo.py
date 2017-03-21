import re

import scrapy

__author__ = 'duydo'

from scrapy.item import Item, Field


class AnyItem(Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value


class XenForoSpider(scrapy.Spider):
    PATTERN_ID = r'(\.){1}(\d+)'
    ID_GROUP = 2
    allowed_domains = []
    _seen_urls = set()

    rules = {
        'forum': '.nodeList .node .nodeInfo .nodeText .nodeTitle a::attr(href)',
        'topic': '.discussionListItems .discussionListItem .listBlock .title a::attr(href)'
    }

    def is_allowed(self, url):
        yes = not self.allowed_domains
        for domain in self.allowed_domains:
            yes = domain in url
        return yes

    def parse(self, response):
        for forum_url in self.parse_forum(response):
            if self.is_allowed(forum_url):
                if forum_url not in self._seen_urls:
                    self._seen_urls.add(forum_url)
                    self.logger.info('[FORUM-%s] %s', self.parse_ID(forum_url), forum_url)
                    yield scrapy.Request(forum_url, callback=self.parse)
                    #
                    # for topic_url in self.parse_topic(response):
                    #     self.logger.info('[TOPIC-%s] %s', self.parse_ID(topic_url), topic_url)

    def parse_forum(self, response):
        forum_rule = self.rules['forum']
        for forum_url in response.css(forum_rule).extract():
            yield response.urljoin(forum_url)

    def parse_topic(self, response):
        for post_url in response.css(self.rules['topic']).extract():
            yield response.urljoin(post_url)

    def parse_message(self, response):
        self.logger.info('Visit: %s', response.url)
        for message in response.css('.messageList .message'):
            message_text = message.css('.messageText::text').extract()
            user_info = message.css('.messageUserInfo a[class ~= username]')
            user_url = user_info.css('::attr(href)').extract()
            user_name = user_info.css('::text').extract()
            message = {
                'url': response.url,
                'content': message_text[0].strip() if message_text else None,
                'user_url': response.urljoin(user_url[0]),
                'user_name': user_name[0].strip()
            }
            yield message

    def parse_ID(self, url, pattern=None, group=2):
        m = re.search(pattern or self.PATTERN_ID, url)
        return m.group(group) if m else None
