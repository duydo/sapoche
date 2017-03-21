import re

import scrapy

__author__ = 'duydo'


class ForumSpider(scrapy.Spider):
    """Forum --1:n--> Topic -> --1:n--> Message"""

    def parse(self, response):
        self.parse_forum(response)

    def parse_forum(self, response):
        pass

    def parse_topic(self, response):
        pass

    def parse_message(self, response):
        pass

    def parse_numbers_from_url(self, url, pattern=None):
        return [int(_) for _ in re.findall(pattern or r'\d+', url)]
