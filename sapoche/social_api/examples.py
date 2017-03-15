from sapoche.social_api.base import OAuth2Api
from sapoche.social_api.facebook import Facebook


def facebook():
    token = '<your access token>',
    fb = Facebook(token)
    """Get information about the owner of the access token"""
    user_id = 'me'
    user = fb.node(user_id)
    print user
    """Get friends of a user"""
    cursor = fb.graph(user_id, 'friends')
    for page in cursor:
        print page


def instagram():
    api = OAuth2Api('https://api.instagram.com/v1')
    api.use_access_token('1723335225.f71bc46.7f63afcbe3a64635b3531ea2c5753ba5')
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
    instagram()
