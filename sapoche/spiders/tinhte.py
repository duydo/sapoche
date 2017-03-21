# -*- coding: utf-8 -*-
from sapoche.spiders.xenforo import XenForoSpider


class OtoSaigonSpider(XenForoSpider):
    name = 'tinhte'
    allowed_domains = ['tinhte.vn']
    start_urls = ['https://tinhte.vn/forums/']
