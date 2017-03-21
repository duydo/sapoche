from scrapy import Item, Field

__author__ = 'duydo'


class Forum(Item):
    id = Field()
    parent_id = Field()
    title = Field()
    url = Field()

