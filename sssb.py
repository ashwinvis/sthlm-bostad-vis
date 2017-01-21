from lxml import html
import pandas as pd

from base import ParserBase
from requests_webkit import Render


class SSSBParser(ParserBase):
    _tag = 'sssb'

    def __init__(self):
        super(SSSBParser, self).__init__()
        self.render = Render()

    def _url(self, area=None, apartment_type='Apartment', max_rent=None, nb_per_page=50):
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
            self.cache_html = self.render.get(url)

    def get(self, using='lxml', xpath='//div[@class="Spreadsheet"]/a/span/text()', **kwargs):
        self._get_html(**kwargs)
        page = self.cache_html
        print('Number of characters in page:', len(page))
        if using == 'lxml':
            tree = html.fromstring(page)
            table = tree.xpath(xpath)
            return tree, table
        elif using == 'pandas':
            table = pd.read_html(page)
            return table
