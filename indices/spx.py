import pandas as pd
import requests


class SPX(object):
    def __init__(self):
        self.data_wiki = None
        self.data_slickcharts = None
        self.html_wiki = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.html_slickcharts = 'https://www.slickcharts.com/sp500'
        pass

    def data_from_wiki(self):
        table_wiki = pd.read_html(self.html_wiki)[0]
        # df_wiki_orig = table_wiki[0]
        df_wiki = table_wiki[['CIK', 'Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']]
        df_wiki = df_wiki.reset_index()
        return df_wiki

    def data_from_slickcharts(self):
        table_slickcharts = pd.read_html(requests.get(self.html_slickcharts,
                                                      headers={'User-agent': 'Mozilla/5.0'}).text)[0]
        df_slickcharts = table_slickcharts[['Symbol', 'Weight']]
        df_slickcharts = df_slickcharts.reset_index()
        dict_slickcharts = df_slickcharts.set_index("Symbol").to_dict(orient='index')
        return dict_slickcharts

    def data_for_indices(self):
        self.data_wiki = self.data_from_wiki()
        self.data_slickcharts = self.data_from_slickcharts()

        for index, row in self.data_wiki.iterrows():
            yield row['CIK'], row['Symbol'], row['Security'], self.data_slickcharts[row['Symbol']]['Weight'], \
                  row['GICS Sector'], row['GICS Sub-Industry']
