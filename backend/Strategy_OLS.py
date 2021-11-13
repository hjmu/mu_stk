from sklearn.linear_model import LinearRegression
from BASE_DB import BASE_DB
import numpy as np
from Utils import *


import webbrowser
from BASE import BASE


class Strategy_OLS(BASE):
    def __init__(self):
        BASE.__init__(self)

        self.stocks = []

    def __init__(self, positiveSlopeThreshold, gt, winsize=3):
        self.positiveSlopeThreshold = positiveSlopeThreshold
        self.gt = gt #1:上走 0:下行
        self.winsize = winsize

    def myplot(self, stcode, stname, x, y, y_new, y_new2, min, max):
        # plot the results
        # plt.figure(figsize=(4, 3))
        ax = plt.axes()
        ax.scatter(x, y)
        ax.plot(x, y_new)
        ax.plot(x, y_new2)
        plt.title(stcode + ' ' + stname, fontproperties=getFont())
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # ax.set_ylim(bottom=0);
        ax.set_ylim([min, max]);
        # ax.axis('tight')
        plt.show()

    def run(self, stcode, stname, df):
        min = df['stclose'].min() - df['stclose'].min()*0.010
        max = df['stclose'].max() + df['stclose'].max()*0.010

        x = df.index.values         #橫軸的值序列
        y = df['stclose'].values    #縱軸的值序列

        #取最新的 winsize 個點
        x1 = df.index.values[-self.winsize:]
        x1 = x1.reshape((-1, 1))
        y1 = df['stclose'].values[-self.winsize:]

        #取 winsize 之前的一段
        x2 = df.index.values[-self.winsize - 14:-self.winsize]
        x2 = x2.reshape((-1, 1))
        y2 = df['stclose'].values[-self.winsize - 14:-self.winsize]

        model = LinearRegression()
        regr = model.fit(x1, y1)

        model2 = LinearRegression()
        regr2 = model2.fit(x2, y2)

        # print(self.gt,stcode,regr.coef_[0],y1)

        y_mean = np.mean(y1)
        slope_norm = regr.coef_[0] / y_mean


        if (
                (self.gt > 0 and regr.coef_[0] > self.positiveSlopeThreshold) #gt>0, 斜率大於 threshold
                or
                (self.gt < 0 and regr.coef_[0] < -self.positiveSlopeThreshold)
        ):
            print(pl(), stcode, stname, regr.coef_[0], y1)
            self.openbrowser(stcode)

            # if (regr.coef_[0] > -0.5 and regr.coef_[0] < 0.5):
            # print(pl(), '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            # print(pl(), '\t',regr.coef_[0], '  ', y_mean, '  ', slope_norm)
            y_new = model.predict(x[:, np.newaxis])
            y_past = model2.predict(x[:, np.newaxis])
            self.myplot(stcode, stname, x, y, y_new, y_past, min, max)



        # df['slope'] = df['stclose'].rolling(Strategy_OLS.winsize).apply(self.moving_slope, raw=False)
        # df['intercept'] = df['stclose'].rolling(Strategy_OLS.winsize).apply(self.moving_intercept, raw=False)
        #
        # df['ma'] = df['stclose'].rolling(Strategy_OLS.winsize).mean()
        # df['slope_norm'] = df['slope'] / df['ma']
        #
        # # df['pct_change'] = df['stclose'].pct_change()
        # # df['pct_change_slope'] = df['pct_change'].rolling(Strategy_OLS.winsize).apply(self.moving_percent_ols,
        # #                                                                               raw=False)
        # slope_norm = df['slope_norm'].iloc[-1]
        #
        # # pct_change_slope = df['pct_change_slope'].iloc[-1]
        # slope = df['slope'].iloc[-1]
        # intercept = df['intercept'].iloc[-1]
        #
        # if (slope_norm > 0):
        #     # print(df)
        #     Strategy_OLS.stocks.append(stcode + ' ' + stname)
        #
        #     x = np.arange(df['stclose'].size)
        #     plt.scatter(x, df['stclose'], c='blue')
        #
        #
        #     abline_values = [slope * i + intercept for i in x]
        #     # Plot the best fit line over the actual values
        #     # plt.plot(x, y, '--')
        #     plt.plot(x, abline_values, 'b')
        #
        #     plt.title(stcode + ' ' + stname + ', ' + str(slope_norm) + "," + "{:10.4f}".format(slope_norm))
        #     plt.show()

    def openbrowser(self,stcode):
        # url = "http://google.com" # 注意:"http://"不可省略

        # url = 'https://tw.stock.yahoo.com/q/ta?s=' + stcode
        url = 'https://pchome.megatime.com.tw/stock/sto0/ock1/sid'+ stcode+'.html'

        # webbrowser.open(url)
        # webbrowser.open_new(url)
        webbrowser.open_new_tab(url)


    def moving_slope(self, values):
        x = np.arange(values.size)
        x = x.reshape((-1, 1))
        model = LinearRegression()
        regr = model.fit(x, values)
        return regr.coef_[0]

    def moving_intercept(self, values):
        x = np.arange(values.size)
        x = x.reshape((-1, 1))
        model = LinearRegression()
        regr = model.fit(x, values)
        return regr.intercept_

    def moving_percent_ols(self, values):
        x = np.arange(values.size)
        x = x.reshape((-1, 1))
        model = LinearRegression()
        regr = model.fit(x, values)

        # print('Coefficients: \n', regr.coef_)
        # print("Model slope:    ", regr.coef_[0])
        # print("Model intercept:", regr.intercept_)

        slope = regr.coef_[0]
        intercept = regr.intercept_
        return slope

    # def lin_regplot(x, y, stcose, stname):
    #     x = x.reshape((-1, 1))
    #     model = LinearRegression()
    #     model.fit(x, y)
    #
    #     plt.scatter(x, y, c='blue')
    #     plt.plot(x, model.predict(x), color='red')
    #     plt.title(stcode + ' ' + stname)
    #     # plt.show()
    #     return

    def abline(self, x, slope, intercept):
        """Plot a line from slope and intercept"""
        # axes = plt.gca()
        # x_vals = np.array(axes.get_xlim())
        # y_vals = intercept + slope * x_vals
        # plt.plot(x_vals, y_vals, '--')

        # ************************************
        # Some dummy data
        # x = [1, 2, 3, 4, 5, 6, 7]
        # y = [1, 3, 3, 2, 5, 7, 9]

        # Find the slope and intercept of the best fit line
        # slope, intercept = np.polyfit(x, y, 1)

        # Create a list of values in the best fit line
        abline_values = [slope * i + intercept for i in x]

        # Plot the best fit line over the actual values
        # plt.plot(x, y, '--')
        plt.plot(x, abline_values, 'b')
        # plt.title(slope)
        # plt.show()


# import matplotlib
if __name__ == "__main__":

    # print(matplotlib.matplotlib_fname())
    # exit(0)

    db = BASE_DB()
    df = db.getStList()
    # print(df)

    n = 1
    for row in df.itertuples():
        stcode = row.stcode
        print(n, ' ', stcode, ' ', row.stname)
        n = n + 1

        stname, df = db.getClosePrices(stcode)
        df = df[["stdate", "stclose"]]

        # df_stclose_zero = df[df['stclose'] == 0.0]
        df = df.drop(df[df['stclose'] == 0.0].index, axis=0)

        # df=df.drop(df['stclose']==0.0,inplace=True, axis=0)
        # df['stclose'] = df['stclose'].replace(0.0, np.nan)
        df['stclose'].fillna(method='ffill', inplace=True)

        # print(df)
        # print(df['stclose'].values[-6:])
        # print(df.index.values[-6:])
        # break;
        # ****************************************************
        if (len(df.index) > 0):
            stra = Strategy_OLS()
            stra.run(stcode, stname, df)
        # break

    print("\n")
    for st in Strategy_OLS.stocks:
        print(st)
