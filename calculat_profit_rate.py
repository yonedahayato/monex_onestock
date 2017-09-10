import sys
import datetime
from get_stock_data import get_data_AfternoonSession
import pandas as pd

def calculate_profit_rate(rate="profit_rate"):
    today = datetime.date.today()
    while True:
        try:
            data_1 = get_data_AfternoonSession(str(today))
            break
        except Exception as e:
            print(str(today)+" is error: {}".format(e))
            today = today - datetime.timedelta(days=1)

    yesterday = today - datetime.timedelta(days=1)
    while True:
        try:
            data_2 = get_data_AfternoonSession(str(yesterday))
            break
        except Exception as e:
            print(str(yesterday)+" is error: {}".format(e))
            yesterday = yesterday - datetime.timedelta(days=1)

    data_1 = data_1.ix[:, ["コード", "銘柄名", "始値"]]
    data_2 = data_2.ix[:, ["コード", "銘柄名", "始値"]]

    data_1 = data_1.rename(columns={"始値": "始値_"+str(today)})
    data_2 = data_2.rename(columns={"始値": "始値_"+str(yesterday)})

    data_1 = data_1.set_index("コード")
    data_2 = data_2.set_index("コード")
    data = pd.concat([data_1, data_2.ix[:, "始値_"+str(yesterday)]], axis=1)
    data = data.dropna()
    data.index = data.index.map(lambda x: x.replace("-T", ""))


    data["diff"] = (data["始値_"+str(today)]-data["始値_"+str(yesterday)])
    data["commision"] = (data.ix[:, "始値_"+str(today)].map(lambda x: max(x*0.005, 48)) + data.ix[:, "始値_"+str(yesterday)].map(lambda x: max(x*0.005, 48)))

    data["profit"] = data["diff"] - data["commision"]
    data["profit_rate"] = data["profit"] / data["始値_"+str(yesterday)]

    if rate=="profit":
        data = data.sort_values(by="profit", ascending=False)
    elif rate=="profit_rate":
        data = data.sort_values(by="profit_rate", ascending=False)
    return data

if __name__ == "__main__":
    data = calculate_profit_rate()
    print(data)
