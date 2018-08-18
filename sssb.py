import os
from io import StringIO
from lxml import html, etree
import pandas as pd
from itertools import chain, islice
import matplotlib.pyplot as plt
from datetime import date

from base import ParserBase

try:
    from requests_selenium import Render
except ImportError:
    from requests_webkit import Render


def ichunked(seq, chunksize):
    """Yields items from an iterator in iterable chunks.

    Parameters
    ----------

    seq : iterable
    chunksize : int

    Returns
    -------
    """
    it = iter(seq)
    for i in it:
        yield chain([i], islice(it, chunksize - 1))


class SSSBParser(ParserBase):
    _tag = "sssb"
    member_since = date(2001, 10, 31)

    def _url(self, area="", apartment_type="Apartment", max_rent="", nb_per_page=50):
        apartment_codes = {"Room": "BOASR", "Studio": "BOAS1", "Apartment": "BOASL"}
        url = (
            r"https://www.sssb.se/en/find-apartment/apply-for-apartment/available-apartments/"
            r"available-apartments-list/?omraden={}&objektTyper={}&hyraMax={}"
            r"&actionId=&paginationantal={}"
        ).format(area, apartment_codes[apartment_type], max_rent, nb_per_page)
        print("Loading", url)
        return url

    def _get_html(self, *args):
        if self._renew_cache():
            url = self._url(*args)
            with Render() as render:
                render = Render()

            self.cache_html = render.get(url)

    def get(self, using="html", *args):
        self._get_html(*args)
        page = self.cache_html
        if using == "html":
            tree = html.fromstring(page)
            return tree
        elif using == "etree":
            xml_parser = etree.HTMLParser()
            tree = etree.parse(StringIO(page), xml_parser)
            return tree

    def make_df(self, tree):
        heading = tree.xpath('//div[@class="RowHeader"]/span/text()')
        rows = tree.xpath('//div[@class="Spreadsheet"]/a/span/text()')
        nb_cols = len(heading)

        def remove_all(seq, match, lstrip=""):
            seq[:] = (value.lstrip(lstrip) for value in seq if value not in match)

        remove_all(rows, (" ", "\xa0", " \xa0"))
        remove_all(heading, "\xa0", " \n")
        nb_cols -= 1
        table = []
        for row in ichunked(rows, nb_cols):
            table.append(tuple(row))

        self.df = pd.DataFrame(table, columns=heading)
        self.df.index = self.df["Address"]

    def make_df_hist(self, store_deltas=True):
        col1 = self.cache_timestamp.strftime("%c")
        col2 = "No. of Applications"

        credit_days = self.df["Credit days"].str.split()
        df_tmp = credit_days.apply(pd.Series)
        df_tmp.columns = [col1, col2]

        # Format and change dtype
        series1 = df_tmp[col1].apply(pd.to_numeric)
        series2 = df_tmp[col2].str.lstrip("(").str.rstrip("st)").apply(pd.to_numeric)
        if self.df_hist is None:
            self.df_hist = pd.DataFrame({col2: series2, "Start": series1})
        else:
            self.df_hist = self.df_hist.T.dropna().T
            if store_deltas:
                self.df_hist[col2] = series2
                delta = series1 - self.df_hist.T.sum() + series2
                self.df_hist[col1] = delta
                if all(delta == 0):
                    return False
            else:
                self.df_hist[col1] = series1
                self.df_hist[col2] = series2

        return True

    def plot_hist(self, save=True, **kwargs):
        plt.style.use("ggplot")
        self.df_hist.iloc[:, 1:].plot(kind="bar", stacked=True, **kwargs)
        plt.subplots_adjust(left=0.075, bottom=0.4, right=0.83, top=0.95)

        plt.legend(loc="best", fontsize=8, bbox_to_anchor=(1.01, 1.0))
        plt.ylabel("Max. credit days")
        plt.autoscale()

        my_credit_days = (date.today() - self.member_since).days
        plt.axhline(y=my_credit_days)

        if save:
            figname = os.path.join(self.path, self._tag + ".png")
            print("Saving", figname)
            plt.savefig(figname)
        else:
            plt.show()
