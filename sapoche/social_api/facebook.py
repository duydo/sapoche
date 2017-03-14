from requests_oauthlib import OAuth2Session

from .base import Api

__author__ = 'duydo'


class Facebook(Api):
    BASE_URL = 'https://graph.facebook.com'
    VERSION = 'v2.8'

    def __init__(self, access_token=None, version=None):
        super(Facebook, self).__init__(
            '%s/%s' % (self.BASE_URL, version or self.VERSION),
            OAuth2Session(token={'access_token': access_token})
        )

    def token(self, access_token):
        self._session.token = {'access_token': access_token}
        return self

    def friends(self, user_id='me', fields=None):
        params = {'fields': fields} if fields else {}
        r = self[user_id].friends.get(params)
        for each in r.data.data:
            yield each
        while 'paging' in r.data:
            params.update({
                'after': r.data.paging.cursors.after
            })
            r = self[user_id].friends.get(params)
            for friend in r.data.data:
                yield friend

    def profile(self, user_id='me', fields=None):
        return self[user_id].get({'fields': fields} if fields else None).data

    def posts(self, user_id='me', params=None):
        params = params or {}
        r = self[user_id].feed.get(params)
        for each in r.data.data:
            yield each
        while 'paging' in r.data:
            r = self[r.data.paging.next].get()
            for each in r.data.data:
                yield each
