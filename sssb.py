from io import StringIO
from lxml import html, etree
import pandas as pd
from itertools import chain, islice

from base import ParserBase
from requests_webkit import Render


def ichunked(seq, chunksize):
    """Yields items from an iterator in iterable chunks."""
    it = iter(seq)
    for i in it:
        yield chain([i], islice(it, chunksize - 1))


class SSSBParser(ParserBase):
    _tag = 'sssb'

    def _url(self, area='', apartment_type='Apartment', max_rent='', nb_per_page=50):
        apartment_codes = {
            'Room': 'BOASR',
            'Studio': 'BOAS1',
            'Apartment': 'BOASL',
        }
        url = (
            r'https://www.sssb.se/en/find-apartment/available-apartments/'
            r'available-apartments-list/?omraden={}&objektTyper={}&hyraMax={}'
            r'&actionId=&paginationantal={}').format(
                area, apartment_codes[apartment_type], max_rent, nb_per_page)

        return url

    def _get_html(self, **kwargs):
        if self._renew_cache():
            url = self._url(**kwargs)
            # with Render() as render:
            render = Render()
            self.cache_html = render.get(url)

    def get(self, using='html', **kwargs):
        self._get_html(**kwargs)
        page = self.cache_html
        print('Number of characters in page:', len(page))
        if using == 'html':
            tree = html.fromstring(page)
            return tree
        elif using == 'etree':
            xml_parser = etree.HTMLParser()
            tree = etree.parse(StringIO(page), xml_parser)
            return tree

    def make_df(self, tree):
        heading = tree.xpath('//div[@class="RowHeader"]/span/text()')
        rows = tree.xpath('//div[@class="Spreadsheet"]/a/span/text()')
        nb_cols = len(heading)

        def remove_all(seq, match, lstrip=''):
            seq[:] = (value.lstrip(lstrip)
                      for value in seq if value not in match)

        remove_all(rows, (' ', '\xa0', ' \xa0'))
        remove_all(heading, '\xa0', ' \n')
        nb_cols -= 1
        table = []
        for row in ichunked(rows, nb_cols):
            table.append(tuple(row))

        self.df = pd.DataFrame(table, columns=heading)
        self.df.index = self.df['Address']

    def make_df_hist(self):
        col1 = self.cache_timestamp.strftime('%c')
        col2 = 'No. of Applications'

        credit_days = self.df['Credit days'].str.split()
        df_tmp = credit_days.apply(pd.Series)
        df_tmp.columns = [col1, col2]

        # Format and change dtype
        series1 = df_tmp[col1].apply(pd.to_numeric)
        series2 = df_tmp[col2].str.lstrip('(').str.rstrip('st)').apply(pd.to_numeric)

        df_tmp[col1] = series1
        df_tmp[col2] = series2

        if self.df_hist is None:
            self.df_hist = df_tmp
        else:
            try:
                self.df_hist = self.df_hist.T.append(df_tmp[col1]).T
                self.df_hist[col2] = df_tmp[col2]
            except KeyError:
                return df_tmp


if __name__ == '__main__':
    if 'parser' not in dir():
        parser = SSSBParser(cache_type='h5')

    tree = parser.get(using='etree')
    parser.make_df(tree)
    df = parser.make_df_hist()
    parser.save()
