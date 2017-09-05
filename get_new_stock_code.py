from urllib2 import *
from lxml import html
import numpy as np
import pandas as pd

base_url = 'http://www.tse.or.jp'

def getTosyo1DataURI():
    contents = urlopen(base_url + '/market/data/listed_companies/index.html').read()
    dom = html.fromstring(contents)

    ep = dom.xpath(u'.//td[contains(text(), "市場第一部 （内国株） ")]')[0].getparent()
    e = ep.xpath('.//a')[0]

    return base_url + e.attrib['href']

def getStockNameDF():
    ds = np.DataSource(None)
    f = ds.open(getTosyo1DataURI())
    df = pd.ExcelFile(f).parse('Sheet1')
    f.close()

    return pd.DataFrame({'code': df[u"コード"].astype('int64'), 'name': df[u"銘柄名"]})

def saveCSV(df):
    df[['code','name']].to_csv('tosyo1.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    data_df = getStockNameDF()
    print(data_df)
