from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from DB import DB
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean

import sys
import os
import time



class Strategy_BollingerBand():
    stocks = []

    def run(self, stcode, stname, df):
        pass

        # Set number of days and standard deviations to use for rolling lookback period for Bollinger band calculation
        window = 5
        no_of_std = 1

        # Calculate rolling mean and standard deviation using number of days set above
        rolling_mean = df['stclose'].rolling(window).mean()
        rolling_std = df['stclose'].rolling(window).std()

        # create two new DataFrame columns to hold values of upper and lower Bollinger bands
        df['Rolling Mean'] = rolling_mean
        df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
        df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)

        df[['stclose', 'Bollinger High', 'Bollinger Low']].plot()
        plt.show()


def bollinger_strat(df, window, std, no_of_std=2):
    rolling_mean = df['Settle'].rolling(window).mean()
    rolling_std = df['Settle'].rolling(window).std()

    df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)

    df['Short'] = None
    df['Long'] = None
    df['Position'] = None

    for row in range(len(df)):

        if (df['Settle'].iloc[row] > df['Bollinger High'].iloc[row]) and (
                df['Settle'].iloc[row - 1] < df['Bollinger High'].iloc[row - 1]):
            df['Position'].iloc[row] = -1

        if (df['Settle'].iloc[row] < df['Bollinger Low'].iloc[row]) and (
                df['Settle'].iloc[row - 1] > df['Bollinger Low'].iloc[row - 1]):
            df['Position'].iloc[row] = 1

    df['Position'].fillna(method='ffill', inplace=True)

    df['Market Return'] = np.log(df['Settle'] / df['Settle'].shift(1))
    df['Strategy Return'] = df['Market Return'] * df['Position']

    df['Strategy Return'].cumsum().plot()


if __name__ == "__main__":

    db = DB()
    db.loadSession()
    df = db.getStList()
    # print(df)

    stcode='1477'
    stname, df = db.getClosePrices(stcode)
    df = df[["stdate", "stclose"]]
    df['stclose'].fillna(method='ffill', inplace=True)

    # ****************************************************
    stra = Strategy_BollingerBand()
    stra.run(stcode, stname, df)

    # print("something")
    # time.sleep(5.5)  # pause 5.5 seconds
    # print("something")

    # sys.exit(0)



    # n = 1
    # for row in df.itertuples():
    #     stcode = row.stcode
    #     print(n, ' ', stcode, ' ', row.stname)
    #     n = n + 1
    #
    #     stname, df = db.getClosePrices(stcode)
    #     df = df[["stdate", "stclose"]]
    #     df['stclose'].fillna(method='ffill', inplace=True)
    #
    #     # ****************************************************
    #     stra = Strategy_BollingerBand()
    #     stra.run(stcode, stname, df)


