import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DB import DB


class Strategy_RSI():

    def RSI(self, series, period):
        # delta = series.diff().dropna()
        delta = series.diff()

        print(delta)
        print('**********************************')
        u = delta * 0
        print(u)
        print('**********************************')
        d = u.copy()
        print(d)
        print('********************************** 11')
        u[delta > 0] = delta[delta > 0]
        print(u)
        print('********************************** 22')
        d[delta < 0] = -delta[delta < 0]
        print(d)

        # u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
        # u = u.drop(u.index[:(period - 1)])
        #
        # d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
        # d = d.drop(d.index[:(period - 1)])
        #
        # # highest weight for the most recent datum points, down to zero.
        # ewma_u = u.ewm(span=period-1).mean()
        # ewma_d = d.ewm(span=period-1).mean()
        # rs=ewma_u/ewma_d

        ma_u = u.rolling(period).mean()
        ma_d = d.rolling(period).mean()
        rs = ma_u / ma_d

        # rsi=100 - 100 / (1 + rs)
        rsi = (ma_u / (ma_u + ma_d)) * 100.0
        return rsi




    # def run(self, stcode, stname, df):
    #     df['diff'] = df['stclose'].diff();
    #     df['u'] = df['diff'] * 0
    #     df['d'] = df['diff'] * 0
    #
    #     df['u'][df['diff'] > 0] = df['diff'][df['diff'] > 0]
    #     df['d'][df['diff'] < 0] = -df['diff'][df['diff'] < 0]
    #
    #     win=5
    #     df['ma_u'] = df['u'].rolling(win).mean()
    #     df['ma_d'] = df['d'].rolling(win).mean()
    #
    #     df['rsi'] = (df['ma_u'] / (df['ma_u'] + df['ma_d'])) * 100.0
    #
    #     # df['RSI'] = self.RSI(df['stclose'], 5)
    #     print(df)

    def run(self, stcode, stname, df):
        df['diff'] = df['stclose'].diff();
        df['u'] = df['diff'] * 0
        df['d'] = df['diff'] * 0

        df['u'][df['diff'] > 0] = df['diff'][df['diff'] > 0]
        df['d'][df['diff'] < 0] = -df['diff'][df['diff'] < 0]

        win=5
        df['ma_u'] = df['u'].rolling(win).mean()
        df['ma_d'] = df['d'].rolling(win).mean()
        df['rsi'] = (df['ma_u'] / (df['ma_u'] + df['ma_d'])) * 100.0

        df['ewma_u'] = df['u'].ewm(span=win, adjust=False).mean()
        df['ewma_d'] = df['d'].ewm(span=win, adjust=False).mean()
        df['rsi2'] = (df['ewma_u'] / (df['ewma_u'] + df['ewma_d'])) * 100.0

        # df['RSI'] = self.RSI(df['stclose'], 5)
        print(df)

if __name__ == "__main__":
    db = DB()
    db.loadSession()
    df = db.getStList()
    # print(df)

    n = 1
    for row in df.itertuples():
        stcode = row.stcode

        if (stcode != '2408'):
            continue

        print(n, ' ', stcode, ' ', row.stname)
        n = n + 1

        stname, df = db.getClosePrices(stcode)

        df = df[["stdate", "stclose"]]

        # df_stclose_zero = df[df['stclose'] == 0.0]
        df = df.drop(df[df['stclose'] == 0.0].index, axis=0)

        # df=df.drop(df['stclose']==0.0,inplace=True, axis=0)
        # df['stclose'] = df['stclose'].replace(0.0, np.nan)
        df['stclose'].fillna(method='ffill', inplace=True)

        # ****************************************************
        if (len(df.index) > 0):
            stra = Strategy_RSI()
            stra.run(stcode, stname, df)
        # break

    # print("\n")
    #     # for st in Strategy_OLS.stocks:
    #     #     print(st)
