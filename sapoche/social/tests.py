from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth2Session

from sapoche.social.api import ApiClient, OAuth1ApiClient
from sapoche.social.providers import ProviderFactory, Provider
from sapoche.social.twitter import UserClient

__author__ = 'duydo'


def twitter_user_client():
    consumer_key = '2aX70JlaiuxqdfDhZ4HZwg'
    consumer_secret = '8R5SebTYnSN2qE5ZxTdarFKsrJtph3EZzYJN55moU'
    access_token_key = '16305268-7zQqtzwOp98SXD1rDk2QJPqdNhatVr7TTsvYLT4HA'
    access_token_secret = 'JzdhSiNRupvpJEKCpLu89js0niMzPA9xoErjS6Es0'

    client = OAuth1ApiClient()
    client.set_auth(consumer_key, consumer_secret, access_token_key, access_token_secret)
    client.set_base_url('https://api.twitter.com/1.1')
    r = client.api['users/show.json'].get(screen_name='duydo')
    print r.data


def instagram():
    url = 'https://api.instagram.com/v1'
    client_id = 'f71bc46bcc5043ca8c675acc547e64c0'
    access_token = '1723335225.f71bc46.7f63afcbe3a64635b3531ea2c5753ba5'
    session = OAuth2Session()
    client = ApiClient(url, session)
    client.set_default_params(access_token=access_token)
    r = client.api['users/1723335225'].get()
    print r.data
    r = client.api['users/25481445/media/recent'].get()
    print r.data


if __name__ == '__main__':
    twitter_user_client()
    # instagram()
