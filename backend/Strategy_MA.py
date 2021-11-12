from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from BASE_DB import BASE_DB
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from BASE import BASE

class Strategy_MA(BASE):
    def __init__(self):
        BASE.__init__(self)
        self.stocks = []

    def run(self, stcode, stname, df):
        df['mashort'] = df['stclose'].rolling(window=3).apply(self.moving_average, raw=False)
        df['malong'] = df['stclose'].rolling(window=10).apply(self.moving_average, raw=False)

        # df['diff'] = df[['mashort','malong']].rolling(1).apply(self.funx, raw=False)
        # df['diff'] = df.rolling(1).apply(self.funxx, raw=False)

        df['diff'] = list(map(self.funx, df['mashort'], df['malong']))
        df['diff1'] = df['diff'].shift(1)

        if (df['diff'].iloc[-1] > 0 and df['diff1'].iloc[-1] < 0):
            print(df)
            Strategy_MA.stocks.append(stcode + ' ' + stname)

            x = np.arange(df['stclose'].size)
            plt.scatter(x, df['stclose'], c='blue')
            plt.plot(x, df['mashort'], label='short')
            plt.plot(x, df['malong'], label='long', linestyle='--')
            plt.title(stcode + ' ' + stname)
            plt.legend(loc='upper left')
            # df[['stclose', 'slope']].plot(figsize=(8, 5),subplots =True)
            plt.show()

        # print(df['mashort'].iloc[-1], ' ', df['malong'].iloc[-1])
        # d1 = df['mashort'].iloc[-1] - df['malong'].iloc[-1]
        # d2 = df['mashort'].iloc[-2] - df['malong'].iloc[-2]
        # if (d1>=0 and d2<0):
        #     print('1')
        # else:
        #     print(-1)

        # df['jj'] = df['stclose'].rolling(5).apply(self.fun, raw=False)
        # df['slope'] = df['stclose'].rolling(5).apply(self.moving_ols, raw=False)

        #         # ddf1["stclose"]=ddf1['stclose'].shift(1)

    # def fun(self, x):
    #     num = 0
    #     for i in x:
    #         # print(i)
    #         num += 1 if i > 10 else 0
    #     return 1 if num >= 2 else -1

    def funx(self, x, y):
        return 1 if x > y else -1

    def moving_average(self, values):
        ma = mean(values)
        return ma

    # def lin_regplot(x, y, stcose, stname):
    #     x = x.reshape((-1, 1))
    #     model = LinearRegression()
    #     model.fit(x, y)
    #
    #     plt.scatter(x, y, c='blue')
    #     plt.plot(x, model.predict(x), color='red')
    #     plt.title(stcode + ' ' + stname)
    #     plt.show()
    #     return


if __name__ == "__main__":

    db = BASE_DB()
    df = db.getStList()
    print(df)

    n = 1
    for row in df.itertuples():
        stcode = row.stcode
        print(n, ' ', stcode, ' ', row.stname)
        n = n + 1

        stname, df = db.getClosePrices(stcode)
        df = df[["stdate", "stclose"]]
        df['stclose'].fillna(method='ffill', inplace=True)

        # ****************************************************
        stra = Strategy_MA()
        stra.run(stcode, stname, df)

    print("\n")
    for st in Strategy_MA.stocks:
        print(st)
