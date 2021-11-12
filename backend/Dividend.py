import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from STModels import Dividend
from Utils import *
import traceback
from STDB import STDB


class Dividends():
    totalDf = pd.DataFrame()

    def getDividentData(self):
        db = STDB()
        df = db.getStList()
        # print(df)

        n = 1
        for row in df.itertuples():
            stockcode = row.stcode
            print(n, ' ', stockcode, ' ', row.stname)
            n = n + 1
            obj = Dividends()
            obj.crawlDivedends(stockcode)

        file = open('pickle_example.pickle', 'wb')
        pickle.dump(Dividends.totalDf, file)
        file.close()

    def crawlDivedends(self, mystcode):
        dfObj = pd.DataFrame(
            columns=['stcode', 'theyear', 'CashDividend', 'EarningDividend', 'ReserveDividend', 'StockDividend',
                     'TotalDividend'])
        # print("Empty Dataframe ", dfObj, sep='\n')

        # with open('a.html', encoding="utf-8") as fp:
        #     soup = BeautifulSoup(fp, 'html.parser')

        url = 'https://tw.stock.yahoo.com/d/s/dividend_' + mystcode + '.html'

        # # 查詢參數
        # my_params = {'q': '寒流'}
        # r = requests.get(google_url, params = my_params)

        r = requests.get(url)

        # print(r.status_code)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            # 觀察 HTML 原始碼
            # print(soup.prettify())

            x = soup.find("td", string="現 金 股 利")
            # print(x)
            # t=soup.find(x,"table")

            rows = x.find_parent("table").find_all("tr")
            # print(rows)
            # rows.pop(0)
            # rows.pop()
            for row in rows[1:]:
                #     print(row)
                cells = row.find_all("td")
                stcode = mystcode
                theyear = int(cells[0].get_text()) + 1911
                CashDividend = float(cells[1].get_text())
                EarningDividend = float(cells[2].get_text())
                ReserveDividend = float(cells[3].get_text())
                StockDividend = float(cells[4].get_text())
                TotalDividend = float(cells[5].get_text())
                dfObj = dfObj.append({'stcode': stcode,
                                      'theyear': theyear,
                                      'CashDividend': CashDividend,
                                      'EarningDividend': EarningDividend,
                                      'ReserveDividend': ReserveDividend,
                                      'StockDividend': StockDividend,
                                      'TotalDividend': TotalDividend},
                                     ignore_index=True)

        # Dividends.totalDf=pd.concat(Dividends.totalDf,dfObj)
        Dividends.totalDf = Dividends.totalDf.append(dfObj)

    def saveDivedends(self):
        db = DB()
        db.loadSession()

        with open('pickle_example.pickle', 'rb') as file:
            df = pickle.load(file)

        try:
            for row in df.itertuples():
                o = Dividend();
                o.stcode = row.stcode
                o.theyear = row.theyear
                o.CashDividend = row.CashDividend
                o.EarningDividend = row.EarningDividend
                o.ReserveDividend = row.ReserveDividend
                o.StockDividend = row.StockDividend
                o.TotalDividend = row.TotalDividend
                DB.session.add(o)
            DB.session.commit()
        except Exception as e:
            DB.session.rollback()
            # var = traceback.format_exc()
            # Utils().info(traceback.format_exc())
            print(pl(),traceback.format_exc())
            # raise


if __name__ == "__main__":
    obj = Dividends()
    obj.getDividentData()
    obj.saveDivedends()

    print("done")
