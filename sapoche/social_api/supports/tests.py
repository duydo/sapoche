from sapoche.social_api.supports.facebook import Facebook


def facebook():
    token = 'EAACEdEose0cBAJLChbBofdQNBxosuSSdd0mYn1l9kyZCDNZBZCjZBMqBcFfm5LrVZCS0oxnZAMAXG4tnYLzFXFCXZA9oKPh6E21aYZBzk7bbrqxRcZBPg722YdnU4GZBpd8FqIKS9uTcp86Koz2WJ11VOAHaMiaNjkdfn9XOd4bea8AFh5jK2EFDThezFs4bZCamMmreTn7O0sd5gZDZD',
    with Facebook(token) as fb:
        cursor = fb.graph('me', 'friends')
        for friends in cursor:
            print friends


if __name__ == '__main__':
    facebook()
