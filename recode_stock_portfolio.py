import pandas as pd
import os.path as path
from pathlib import Path

class management_portfolio:
    def __init__(self):
        self.file_name = "./recode_portfolio.csv"
        if not path.exists(self.file_name):
            self.isfile = False
        else:
            self.isfile = True
            self.recode_df = pd.read_csv(self.file_name, header=0)
            self.recode_df[["code"]] = self.recode_df[["code"]].astype(str)
            self.recode_df[["status"]] = self.recode_df[["status"]].astype(str)

    def recode_stock_portfolio(self, status, code, number, price="NaN"):
        if status == "buy":
            print("recode about buy")
            recode_df = pd.DataFrame({"code": [str(code)], "status": [status], "number": [number], "price": [price]})
            recode_df = recode_df[["code", "status", "number", "price"]]

            if self.isfile:
                self.recode_df = pd.concat([self.recode_df, recode_df])
            else:
                self.recode_df = recode_df

        elif status == "sell":
            print("recode about sell")
            print(self.recode_df)
            sell_code_status = self.recode_df.ix[(self.recode_df.ix[:, "code"]==str(code)) & (sself.recode_df.ix[:, "status"]=="buy"), "status"]
            sell_code_index = sell_code_status.index[0]
            print(sell_code_status)

            if sell_code_status.empty:
                raise Exception("you can`t sell this code. sell_code_status is empty")
            elif len(sell_code_status) != 1:
                raise Exception("you can`t sell this code. sell_code_status`s len is not 1")
            else:
                sell_code_status = sell_code_status.values[0]
                print(sell_code_status)

            print(sell_code_status)

            if sell_code_status == "buy":
                self.recode_df.ix[sell_code_index, "status"] = "sell"

            else:
                raise Exception("you can`t sell this code. this code`s status is not sell")

        else:
            raise Exception("recode_stock_portfolio error: status is invalid")

        self.ToCsv()

    def ToCsv(self):
        print(self.recode_df)
        self.recode_df.to_csv(self.file_name, index=False, header=True)

if __name__ == "__main__":
    mf = management_portfolio()
    mf.recode_stock_portfolio("buy", "9976", 1)
    mf.recode_stock_portfolio("sell", "9976", 1)
