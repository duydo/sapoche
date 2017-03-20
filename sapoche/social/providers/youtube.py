from ..api import SocialApi

__author__ = 'duydo'


class Youtube(SocialApi):
    """Youtube Data API
    See https://developers.google.com/youtube/v3/docs/
    """
    BASE_URL = 'https://www.googleapis.com/youtube'
    VERSION = '3'

    def __init__(self, access_token, version=None):
        super(Youtube, self).__init__(
            base_url='%s/v%s' % (self.BASE_URL, version or self.VERSION),
            access_token=access_token
        )
