from sapoche.social_api.base import OAuth2Api

__author__ = 'duydo'


class Instagram(OAuth2Api):
    BASE_URL = 'https://api.instagram.com'
    VERSION = 'v1'

    def __init__(self, access_token=None, version=None):
        super(Instagram, self).__init__('%s/%s' % (self.BASE_URL, version or self.VERSION))
        self.use_access_token(access_token)
