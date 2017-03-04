import sys

__author__ = 'duydo'

__all_ = ['Provider', 'ProviderFactory']


class Provider(object):
    TWITTER = 'twitter'
    FACEBOOK = 'facebook'
    INSTAGRAM = 'instagram'


class ProviderFactory(object):
    SUPPORTED_DRIVERS = {
        Provider.FACEBOOK: (1, 2),
        Provider.TWITTER: (1, 2),
        Provider.INSTAGRAM: (1, 2)
    }
    drivers = SUPPORTED_DRIVERS.copy()

    def get(self, provider):
        return self.drivers.get(provider)

    def set(self, provider, module, clazz):
        self.drivers[provider] = (module, clazz)
        try:
            driver = self.get(provider)
        except (ImportError, AttributeError):
            self.drivers.pop(provider)
            exp = sys.exc_info()[1]
            raise exp

        return driver
