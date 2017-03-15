from sapoche.social_api.base import ApiException
from sapoche.social_api.facebook import Facebook

token = '',
with Facebook(token) as fb:
    try:
        cursor = fb.graph('me', 'friends')
        for friends in cursor:
            print friends
    except ApiException as e:
        print e.message
