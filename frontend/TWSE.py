# coding: utf-8
#

import os,sys
from environs import Env
from loguru import logger
import datetime
import pandas as pd
import re
# from Utils import Utils
import traceback
# from CONST import  *

from BASE import BASE


class TWSE(BASE):
    def __init__(self):
        BASE.__init__(self)


# class TWSE(BASE):
#     def __init__(self):
#         env = Env()
#         env.read_env(path='../.myenv')
#         FRONT_LOG_FILE = env.str('FRONT_LOG_FILE')
#         LOG_FMT=env.str('LOG_FMT')
#         logger.add(sys.stderr, format=LOG_FMT)
#         logger.add(FRONT_LOG_FILE, format=LOG_FMT)
#
#         self.TWSE_CSV_FILE = env.str("TWSE_CSV_FILE")

    def fetch(self):
        url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=csv"
        cols = ['stockcode', 'stockname', 'volumn', 'amount', 'open', 'high', 'low', 'close', 's1', 's2', 's3']
        df = pd.read_csv(url, encoding="mbcs", names=cols)
        return df

    def getDate(self,s):
        regex = re.compile(r'(\d+)年(\d+)月(\d+)日')
        match = regex.search(s)
        # print(match.group(1)+','+match.group(2)+','+match.group(3))
        year = int(match.group(1)) + 1911
        dt = datetime.date(year, int(match.group(2)), int(match.group(3))).strftime('%Y-%m-%d')
        # dt=datetime.date(2015, 1, 12).strftime('%Y-%m-%d')
        # dt=datetime.datetime.today().strftime('%Y-%m-%d')
        return dt


    def getCleanCode(self,s):
        s=s.replace('"','')
        s=s.replace('=','')
        return s

    # 抓當日股價
    def getdata(self):
        try:
            # get today's data from twse
            df = self.fetch()
            # print(df['stockcode'][0])

            # convert "108年11月08日 當日日成交資訊 (股) to 2019-11-08"
            thedate = self.getDate(df['stockcode'][0])
            # print(thedate)

            # remove top rows and buttom rows
            df2 = df.loc[2:len(df) - 4, 'stockcode':'close']
            # print(df2)

            df2['stockcode'] = df2['stockcode'].apply(lambda x: self.getCleanCode(x))
            # print(df2)

            # df2.to_csv("c:/temp/ST_" + thedate + ".csv", sep=',', encoding='mbcs', index=False)
            # df2.to_csv(self.TWSE_CSV_FILE_PREIX + thedate + ".csv", sep=',', encoding='utf-8', index=False)
            df2.to_csv(self.TWSE_CSV_FILE, sep=',', encoding='utf-8', index=False)
            return thedate, df2
        except Exception as e:
            # print(e)
            # Utils().info(traceback.format_exc())
            logger().info(traceback.format_exc())

if __name__ == "__main__":
    thedate, df = TWSE().getdata()