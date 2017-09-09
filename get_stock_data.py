import sys
import pandas as pd
import urllib.request as request
from io import StringIO

def get_data_AfternoonSession(date):
    csv_url = "http://k-db.com/stocks/"+str(date)+"/b?download=csv"
    res = request.urlopen(csv_url)
    data = res.read().decode("shift-jis")
    data_df = pd.read_csv(StringIO(data))
    data_df = data_df.ix[data_df["市場"]=="東証1部", :]
    data_df = data_df.reset_index(drop=True)
    print("len(data_df): {}".format(len(data_df)))
    return data_df

if __name__ == "__main__":
    get_data_AfternoonSession("2017-09-06")
