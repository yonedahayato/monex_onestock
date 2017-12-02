import pandas as pd
import os.path as path
from pathlib import Path

class management_portfolio:
    def __init__(self, recode_save_path=None):
        if recode_save_path == None:
            self.file_name = "./recode_portfolio.csv"
        else:
            self.file_name = recode_save_path

        if not path.exists(self.file_name):
            self.isfile = False
        else:
            self.isfile = True
            self.recode_df = pd.read_csv(self.file_name, header=0)
            self.recode_df[["code"]] = self.recode_df[["code"]].astype(str)
            self.recode_df[["status"]] = self.recode_df[["status"]].astype(str)

        self.sell_possible_list = None

    def recode_stock_portfolio(self, status, code, number, price="NaN", profit="NaN", profit_rate="NaN"):
        if status == "buy":
            print("recode about buy")
            recode_df = pd.DataFrame({"code": [str(code)], "status": [status], "number": [number], "price": [price], "profit": [profit], "profit_rate": [profit_rate]})
            recode_df = recode_df[["code", "status", "number", "price", "profit", "profit_rate"]]

            if self.isfile:
                self.recode_df = pd.concat([self.recode_df, recode_df])
            else:
                self.recode_df = recode_df

        elif status == "sell":
            if not self.isfile:
                raise("not error. but there are not recode save file")

            print("recode about sell")
            print(self.recode_df)
            sell_code_status = self.recode_df.ix[(self.recode_df.ix[:, "code"]==str(code)) & (self.recode_df.ix[:, "status"]=="buy"), "status"]
            sell_code_index = sell_code_status.index[0]

            if sell_code_status.empty:
                raise Exception("you can`t sell this code. sell_code_status is empty")
            elif len(sell_code_status) != 1:
                raise Exception("you can`t sell this code. sell_code_status`s len is not 1")
            else:
                sell_code_status = sell_code_status.values[0]

            print(sell_code_status)

            if sell_code_status == "buy":
                self.recode_df.ix[sell_code_index, "status"] = "sell"

            else:
                raise Exception("you can`t sell this code. this code`s status is not sell")

        else:
            raise Exception("recode_stock_portfolio error: status is invalid")

        self.ToCsv()

    def ToCsv(self):
        self.recode_df.to_csv(self.file_name, index=False, header=True)
        self.isfile = True

    def sell_possible_code(self):
        if not self.isfile:
            raise("not error. but there are not recode save file")

        sell_possible_list = self.recode_df.ix[self.recode_df.ix[:, "status"]=="buy", :]
        if len(sell_possible_list) == 1:
            sell_possible_code = sell_possible_list.ix[:, "code"]
            sell_possible_code = sell_possible_code.values[0]
            return sell_possible_code
        elif len(sell_possible_list) == 0:
            raise Exception("sell possible list is empty")
        else:
            print(sell_possible_list)
            raise Exception("sell possible code is multiple")

if __name__ == "__main__":
    mf = management_portfolio()
    mf.recode_stock_portfolio("buy", "1332", 1)
    mf.recode_stock_portfolio("sell", "1332", 1)
    mf.recode_stock_portfolio("buy", "9976", 1)
    mf.recode_stock_portfolio("sell", "9976", 1)
