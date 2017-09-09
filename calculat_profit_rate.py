import sys
import datetime
from get_stock_data import get_data_AfternoonSession
import pandas as pd

def calculate_profit_rate(rate="profit_rate"):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)

    data_1 = get_data_AfternoonSession(str(yesterday))
    data_2 = get_data_AfternoonSession(str(day_before_yesterday))

    data_1 = data_1.ix[:, ["コード", "銘柄名", "始値"]]
    data_2 = data_2.ix[:, ["コード", "銘柄名", "始値"]]

    data_1 = data_1.rename(columns={"始値": "始値_"+str(yesterday)})
    data_2 = data_2.rename(columns={"始値": "始値_"+str(day_before_yesterday)})

    data_1 = data_1.set_index("コード")
    data_2 = data_2.set_index("コード")
    data = pd.concat([data_1, data_2.ix[:, "始値_"+str(day_before_yesterday)]], axis=1)
    data = data.dropna()

    data["diff"] = (data["始値_"+str(yesterday)]-data["始値_"+str(day_before_yesterday)])
    data["commision"] = (data.ix[:, "始値_"+str(yesterday)].map(lambda x: max(x*0.005, 48)) + data.ix[:, "始値_"+str(day_before_yesterday)].map(lambda x: max(x*0.005, 48)))
    data["profit"] = data["diff"] - data["commision"]
    data["profit_rate"] = data["profit"] / data["始値_"+str(day_before_yesterday)]
    if rate=="profit":
        data = data.sort_values(by="profit", ascending=False)
    elif rate=="profit_rate":
        data = data.sort_values(by="profit_rate", ascending=False)

    return data

if __name__ == "__main__":
    data = calculate_profit_rate()
    print(data)
