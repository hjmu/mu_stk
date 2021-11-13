import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib as matplotlib
import matplotlib.pyplot as plt
from BASE_DB import BASE_DB
import pandas as pd
from Utils import *

# from Utils import Logger
from backend.Strategy_OLS import Strategy_OLS
from backend.Strategy_MA import Strategy_MA
# from CONST import *
from BASE import BASE


class Main_Backend(BASE):
    def __init__(self):
        BASE.__init__(self)

    def doOLS(self,stcode, stname, df):
        # stra = Strategy_OLS()
        Strategy_OLS(self.OLS_SLOPE, self.OLS_DIRECTION, 3).run(stcode, stname
                                                                ,df #此 stock 的資料
                                                                )

    def doMA(self,stcode, stname, df):
        stra = Strategy_MA()
        stra.run(stcode, stname, df)

    def main(self):
        # print(matplotlib.matplotlib_fname())
        # exit(0)

        db = BASE_DB()
        df_stks = db.getStList()
        # print(df_stks)

        for i, row in enumerate(df_stks.itertuples(), 1):
            # print(i, row.name)
        # n = 1
        # for row in df_stks.itertuples():
            stcode = row.stcode
            stname = row.stname

            # n = n + 1

            df = db.getClosePrices(stcode)
            # df = df.iloc[-300:]

            df = df[["stdate", "stclose", "stvol"]]
            df.drop(df[df['stclose'] == 0.0].index, inplace=True, axis=0)
            df['stclose'].fillna(method='ffill', inplace=True)

            # if stcode=='2303':
            #     print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
            if (len(df.index) <= 0):
                # print(pl(), stcode, stname, ',len <0, skip')
                continue

            # 成交量 < 1000 張
            vol = df['stvol'].values[-1:] / 1000
            if (vol < 1000):
                # print(pl(), stcode, stname, '  vol ', vol,' low, skip')
                continue;

            # 股價 <10 或 >200
            price = df['stclose'].values[-1:]
            if (price < 10 or price > 200):
                # print(pl(), stcode, stname, '  price ', price, ' out of range, skip')
                continue;

            # print(pl(), stcode, " ", price, " ", vol)

            # print(df)
            # print(df['stclose'].values[-6:])
            # print(df.index.values[-6:])
            # break;
            # ****************************************************
            # if (len(df.index) > 0):
            # print(df)
            # break

            print(pl(), i, df_stks.shape[0], '_' + stcode + ',', stname)
            self.doOLS(stcode, stname, df)

        # print("\n")
        # for st in Strategy_OLS.stocks:
        #     print(st)


    # print("MMMMxxx==>"+stname)
    # print(matplotlib.matplotlib_fname())

if __name__ == "__main__":
    Main_Backend().main()
