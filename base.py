import os
from time import time
from datetime import datetime
import requests
import pandas as pd
from inspect import getmembers
from functools import partialmethod


class ParserBase(object):
    def __init__(self):
        self.df = pd.DataFrame()
        self.df_hist = pd.DataFrame()
        self.path = os.path.join(os.path.curdir, 'cache')
        self.cache_html = ''
        self.cache_timestamp = None
        self.cache_update_after = 15 * 60  # in seconds
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
            page = requests.get(url)
            self.cache_html = page.content

    def _cache_filename(self, ext):
        fn = os.path.join(self.path, self._tag + ext)
        fn_hist = os.path.join(self.path, self._tag + '_hist' + ext)
        return fn, fn_hist

    def _save(self, ext, func):
        fn, fn_hist = self._cache_filename(ext)
        self.df.__getattr__(func)(fn)
        self.df_hist.__getattr__(func)(fn_hist)

    def _load(self, ext, func):
        fn, fn_hist = self._cache_filename(ext)
        load_func = dict(getmembers(pd))[func]
        self.df = load_func(fn)
        self.df_hist = load_func(fn_hist)

    save_csv = partialmethod(_save, '.csv', 'to_csv')
    save_json = partialmethod(_save, '.json', 'to_json')
    load_csv = partialmethod(_load, '.csv', 'read_csv')
    load_json = partialmethod(_load, '.json', 'read_json')
