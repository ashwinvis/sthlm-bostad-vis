import os
from time import time
from datetime import datetime
import requests
import pandas as pd


class ParserBase(object):
    def __init__(self):
        self.df = pd.DataFrame()
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

    def save_csv(self):
        fn = os.path.join(self.path, self._tag + '.csv')
        self.df.to_csv(fn)

    def save_json(self):
        fn = os.path.join(self.path, self._tag + '.json')
        self.df.to_json(fn)

    def load_csv(self):
        fn = os.path.join(self.path, self._tag + '.csv')
        self.df = pd.read_csv(fn)

    def load_json(self):
        fn = os.path.join(self.path, self._tag + '.json')
        self.df = pd.read_json(fn)
