import os
from time import time
from datetime import datetime
import pandas as pd
from inspect import getmembers
from functools import partialmethod
try:
    from urllib import request
    URLLIB = True
except ImportError:
    import requests
    URLLIB = False


def _dict(obj):
    # return obj.__dict__  # Python 2
    return dict(getmembers(obj))


class ParserBase(object):
    _tag = 'base'

    def __init__(self, cache_type='h5', *args):
        self.path = os.path.join(os.path.curdir, 'cache')
        fn, fn_hist = self._cache_filename('.' + cache_type)
        self.cache_type = cache_type
        self.cache_html = ''
        self.cache_timestamp = None
        self.cache_update_after = 15 * 60  # in seconds

        if os.path.exists(fn) and os.path.exists(fn_hist):
            self.load()
        else:
            self.df = None
            self.df_hist = None

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def _url(*args):
        return r'http://www.example.com'

    def _renew_cache(self):
        if self.cache_timestamp is None:
            self.cache_timestamp = datetime.fromtimestamp(time())
            return True
        else:
            now_timestamp = datetime.fromtimestamp(time())
            dt = now_timestamp - self.cache_timestamp
            if dt.seconds > self.cache_update_after:
                self.cache_timestamp = now_timestamp
                return True
            else:
                return False

    def _get_html(self, *args):
        if self._renew_cache():
            url = self._url(*args)
            if URLLIB:
                with request.urlopen(url) as response:
                    html = response.read()
            else:
                html = requests.get(url).content

            self.cache_html = html

    def _cache_filename(self, ext):
        fn = os.path.join(self.path, self._tag + ext)
        fn_hist = os.path.join(self.path, self._tag + '_hist' + ext)
        return fn, fn_hist

    def _save(self, ext, func, **kwargs):
        fn, fn_hist = self._cache_filename(ext)
        self.df.__getattr__(func)(fn, **kwargs)
        self.df_hist.__getattr__(func)(fn_hist, **kwargs)

    def _load(self, ext, func, **kwargs):
        fn, fn_hist = self._cache_filename(ext)
        load_func = _dict(pd)[func]
        self.df = load_func(fn, **kwargs)
        self.df_hist = load_func(fn_hist, **kwargs)

    save_csv = partialmethod(_save, '.csv', 'to_csv')
    save_json = partialmethod(_save, '.json', 'to_json')
    save_h5 = partialmethod(_save, '.h5', 'to_hdf', key=_tag, format='table')
    load_csv = partialmethod(_load, '.csv', 'read_csv')
    load_json = partialmethod(_load, '.json', 'read_json')
    load_h5 = partialmethod(_load, '.h5', 'read_hdf', key=_tag, format='table')

    def save(self):
        _dict(self)['save_' + self.cache_type]()

    def load(self):
        _dict(self)['load_' + self.cache_type]()
