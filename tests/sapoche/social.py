import unittest
import logging

from sapoche.social.api import SocialApi, TokenPlace
from sapoche.social.providers import Instagram
from sapoche.social.providers.youtube import Youtube

__author__ = 'duydo'

logging.basicConfig(level=logging.ERROR)


class SocialApiTest(unittest.TestCase):
    def test_instagram_api(self):
        access_token = '1723335225.f71bc46.7f63afcbe3a64635b3531ea2c5753ba5'

        # base_url = 'https://api.instagram.com/v1'
        # api = SocialApi(base_url, access_token, access_token_place=TokenPlace.QUERY)
        # or
        api = Instagram(access_token)

        """/users/self"""
        r = api.users.self()

        b = r.body
        self.assertEqual(b.data.id, '1723335225')
        self.assertEqual(b.data.username, 'duy.dq')

        """/users/<user-id>"""
        r = api.users['1723335225']()
        self.assertEqual(r.body.data.id, '1723335225')

        """/users/<user-id>/media/recent"""
        r = api.users['1723335225'].media.recent()
        self.assertTrue(len(r.body.data) >= 1)

        """/users/search?q=<query>"""
        r = api.users.search({'q': 'duy'})
        self.assertTrue(len(r.body.data) >= 1)

    def youtube(self):
        access_token = '<your access token>'
        api = Youtube(access_token)
        r = api.videos({'id': 'JGwWNGJdvx8', 'part': 'statistics'})
        for item in r.body.data['items']:
            print item.statistics


if __name__ == '__main__':
    unittest.main()
