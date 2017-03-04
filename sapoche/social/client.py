__author__ = 'duydo'


class SocialClient(object):
    def get_profile(self, *args, **kwargs):
        pass

    def get_connections(self, *args, **kwargs):
        pass

    def get_activities(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    sc = SocialClient()
    sc.profile()
    sc.posts()
