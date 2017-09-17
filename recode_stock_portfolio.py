import pandas as pd
import os.path as path
from pathlib import Path

def recode_stock_portfolio(status, code, number, price="nan"):
    file_name = "./recode_portfolio.csv"
    if not path.exists(file_name):
        Path("./recode_portfolio.csv").touch()

    recode_df = pd.read_csv(file_name, header=True)
    recode_df = pd.concat([recode_df, pd.DataFrame({"code": [code], "status": [status], "number": [number], "price": [price]})])

    recode_df.to_csv(file_name, index=False, header=True)


if __name__ == "__main__":
    recode_stock_portfolio()
