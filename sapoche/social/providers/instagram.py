from ..api import SocialApi, TokenPlace

__author__ = 'duydo'


class Instagram(SocialApi):
    """Instagram API.
    See https://www.instagram.com/developer/endpoints/
    """
    BASE_URL = 'https://api.instagram.com'
    VERSION = '1'

    def __init__(self, access_token, version=None):
        super(Instagram, self).__init__(
            base_url='%s/v%s' % (self.BASE_URL, version or self.VERSION),
            access_token=access_token,
            access_token_place=TokenPlace.QUERY
        )
