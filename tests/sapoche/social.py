import unittest
import logging

from sapoche.social.api import SocialApi, TokenPlace

__author__ = 'duydo'

logging.basicConfig(level=logging.DEBUG)


class SocialApiTest(unittest.TestCase):
    def test_instagram_api(self):
        base_url = 'https://api.instagram.com/v1'
        access_token = '1723335225.f71bc46.7f63afcbe3a64635b3531ea2c5753ba5'

        api = SocialApi(base_url, access_token, access_token_place=TokenPlace.QUERY)

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

    def test_youtube(self):
        key = 'AIzaSyA3WjUxG2OG7Lkwze8_e8rqEt3xOkSWqKo'
        api = SocialApi('https://www.googleapis.com/youtube/v3')
        params = {
            'id': 'JGwWNGJdvx8',
            'part': 'statistics',
            'key': key
        }
        r = api.videos(params)
        for item in r.data['items']:
            print item.statistics


if __name__ == '__main__':
    unittest.main()
