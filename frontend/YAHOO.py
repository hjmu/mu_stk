# coding: utf-8
#
import datetime
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
# from DB2 import DB2
# import STDB as STDB
from BASE import BASE

class YAHOO(BASE):
    def __init__(self):
        BASE.__init__(self)


    def getEps(self, s):
        if s==None:return None

        regex = re.compile(r'(.+)元')
        match = regex.search(s)
        # print(match.group(1)+','+match.group(2)+','+match.group(3))
        # year = int(match.group(1))
        if match:
            return match.group(1)
        else:
            return None

    def getCleanCode(self, s):
        s = s.replace('"', '')
        s = s.replace('=', '')
        return s

    # 抓
    def getQuarterlyEPS(self, stcode):
        url = "https://tw.stock.yahoo.com/d/s/company_" + stcode + ".html"

        # 使用requests.get() 來得到網頁回傳內容
        r = requests.get(url)

        # request.get()回傳的是一個物件
        # 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
        web_content = r.text

        # 以 Beautiful Soup 解析 HTML 程式碼 :
        soup = BeautifulSoup(web_content, 'html.parser')

        x1, x2, x3, x4 = None, None, None, None
        if soup.find("td", text="109第3季"):
            x1 = soup.find("td", text="109第3季").find_next_sibling("td").text
        if soup.find("td", text="109第2季"):
            x2 = soup.find("td", text="109第2季").find_next_sibling("td").text
        if soup.find("td", text="109第1季"):
            x3 = soup.find("td", text="109第1季").find_next_sibling("td").text
        if soup.find("td", text="108第4季"):
            x4 = soup.find("td", text="108第4季").find_next_sibling("td").text

        print('---->', stcode, x1, x2, x3, x4)

        x1 = self.getEps(x1)
        x2 = self.getEps(x2)
        x3 = self.getEps(x3)
        x4 = self.getEps(x4)

        # print(x1, x2, x3, x4)

        return x1, x2, x3, x4


if __name__ == "__main__":

    db = BASE()
    df = db.getStList()
    # print(df)

    n = 1

    for row in df.itertuples():
        stcode = row.stcode
        x1, x2, x3, x4 = YAHOO().getQuarterlyEPS(stcode)
        print(n,stcode, x1, x2, x3, x4)
        n += 1
        # if n == 30: break
        if (x1):
            db.insertQuarterEps(stcode, '2020_3', x1)
        if (x2):
            db.insertQuarterEps(stcode, '2020_2', x2)
        if (x3):
            db.insertQuarterEps(stcode, '2020_1', x3)
        if (x4):
            db.insertQuarterEps(stcode, '2019_4', x4)
