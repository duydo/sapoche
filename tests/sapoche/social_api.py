from sapoche.social_api.base import OAuth2Api
from sapoche.social_api.providers import Facebook, Instagram

__author__ = 'duydo'


def facebook():
    token = 'EAACEdEose0cBAGZC2L69XZBmHKkBcmVzQESZCmMfBFlfXgQ38sKUZA3LSLvT0D92tVbc5nqFMZCDTzhV0nC5qxrZBbdPLOIblBOVmyhtFBpcYlT4KnuyVkbCoetZAi7rO4nsbtO1FtfrrhmJFyUTlgKYWXZAuhSAMyO0QjdkGIEWrN3KCyCdyVYGTZB7g8FlMfq5APVeRpKxwOAZDZD',
    fb = Facebook(token)
    r = fb.node('me', fields='id,name,friends')
    for friends in fb.paging(r.friends):
        print friends


def instagram():
    api = Instagram('1723335225.f71bc46.7f63afcbe3a64635b3531ea2c5753ba5')
    """Get information about the owner of the access token: /users/self"""
    response = api.users.self.get().data
    print response

    """Get information about a user: /users/user-id"""
    response = api.users['1723335225'].get().data
    print response

    """Get most recent media published by a user: /users/user-id/media/recent"""
    response = api.users['1723335225'].media.recent.get().data
    print response

    """Get a list of users matching the query: /users/search?q=trung"""
    response = api.users.search.get({'q': 'trung'}).data
    print response


if __name__ == '__main__':
    youtube = OAuth2Api('https://www.googleapis.com/youtube/v3')
    params = {
        'id': 'JGwWNGJdvx8',
        'part': 'statistics',
        'key': 'AIzaSyA3WjUxG2OG7Lkwze8_e8rqEt3xOkSWqKo'
    }
    r = youtube.videos.get(params)
    for item in r.data['items']:
        print item.statistics
