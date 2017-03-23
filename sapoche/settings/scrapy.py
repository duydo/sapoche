LOG_LEVEL = 'INFO'
BOT_NAME = 'sapoche'
SPIDER_MODULES = ['sapoche.spiders']
NEWSPIDER_MODULE = 'sapoche.spiders'

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': USER_AGENT,
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,*'
}
