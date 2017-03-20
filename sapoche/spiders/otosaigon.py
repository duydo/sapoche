# -*- coding: utf-8 -*-
from sapoche.spiders.xenforo import XenForoSpider


class OtoSaigonSpider(XenForoSpider):
    name = 'otosaigon'
    allowed_domains = ['otosaigon.com']
    start_urls = ['https://otosaigon.com/forums/']
