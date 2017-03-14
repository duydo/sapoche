from requests_oauthlib import OAuth2Session

from sapoche.social_api.facebook import Facebook


def facebook():
    token = 'EAACEdEose0cBADg8mUZBMYyY0W7TBPKoaw87XUEZApTRQbGGWE2OpCrlHqYPzvzzVB9rtdg4Y78auQDMnSfP3adg6pdlN4jofPlvVlgIBtpJcXwpIRGuAPotZASBV1VkwZCncYYCOLHxPKyquxjI07542CVuApwIpsS8e6cX4eDFIUv5gJopdjGzkxX1lC5rxpNl3lwW2QZDZD',
    with Facebook(token) as fb:
        p = fb.profile()
        print p
        friends = fb.friends()
        for each in friends:
            print each
        posts = fb.posts()
        for each in posts:
            print each


if __name__ == '__main__':
    facebook()
