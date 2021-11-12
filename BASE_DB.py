import os,sys
from environs import Env
from loguru import logger
import numpy as np
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from STModels import Stmaster
from STModels import Stdatum
import traceback
from BASE import BASE

class BASE_DB(BASE):
    def __init__(self):
        BASE.__init__(self)
        # env = Env()
        # env.read_env(path='../.myenv')
        # FRONT_LOG_FILE = env.str('FRONT_LOG_FILE')
        # LOG_FMT=env.str('LOG_FMT')
        # logger.add(sys.stderr, format=LOG_FMT)
        # logger.add(FRONT_LOG_FILE, format=LOG_FMT)


        self.engine = create_engine('sqlite:///%s' % self.DB_PATH, echo=None)
        # engine = create_engine("mysql+mysqlconnector://chao:chao123@127.0.0.1:3306/st", max_overflow=5,echo=True)
        # engine = create_engine("mysql+mysqlconnector://chao:chao123@127.0.0.1:3306/st")
        # engine = create_engine("mysql+mysqldb://chao:chao123@127.0.0.1:3306/st")

        self.metadata = MetaData(self.engine)
        # myfaq = Table('faq', metadata, autoload=True)
        # mapper(faq, myfaq)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def getStList(self):
        # for instance in session.query(Stmaster).order_by(Stmaster.stcode):
        #     print(instance.stcode, instance.stname)
        df = pd.read_sql(self.session.query(Stmaster).order_by(Stmaster.stcode).statement, self.session.bind)
        return df

    def getClosePrices(self, stcode):
        # y = np.array()
        # n=1
        # num=[]
        # price = []
        # for instance in session.query(Stdatum).filter(Stdatum.stcode==stcode).order_by(Stdatum.stdate):
        #     print(instance.stcode,instance.stdate, instance.stclose)
        #     num.append(n)
        #     n += 1
        #     price.append(instance.stclose)
        #
        # x=np.array(list(reversed(num)))
        # y = np.array(list(reversed(price)))
        # print(x)
        # print(y)
        #
        # df = pd.read_sql(query.statement, query.session.bind)
        # df=pd.read_sql("SELECT stdate,stopen,stclose,stvol FROM stdata where stcode='" + stcode +"'", self.session.bind)
        # df=pd.read_sql(session.query(Stdatum).filter(Stdatum.stcode==stcode).statement, session.bind)
        sql_sub = "SELECT * FROM stdata where stcode='" + stcode + "' order by stdate desc limit " + str(self.REC_LIMIT)
        sql = "SELECT stdate,stopen,stclose,stvol FROM (" + sql_sub + ") order by stdate"
        # sql="SELECT stdate,stopen,stclose,stvol FROM stdata where stcode='" + stcode +"'"

        # print(pl(), sql)

        df = self.getDF(sql)

        # df2 = pd.read_sql("SELECT stname FROM stmaster where stcode='" + stcode + "'", self.session.bind)
        # df2 = self.getDF("SELECT stname FROM stmaster where stcode='" + stcode + "'")
        # stname=df2["stname"][0]

        # session.query(Stmaster).filter(Stmaster.stcode == stcode)
        return df

        # for index in range(len(price),0,-1):
        #     print(price[index-1])

    def getDF(self, sql):
        df = pd.read_sql(sql, self.session.bind)
        return df

    def insertMaster(self, df):
        for row in df.itertuples():
            # print("~~"+row.stockcode+","+row.volumn.replace(',','')+","+row.amount.replace(',',''))
            exists = self.session.query(Stmaster.stcode).filter_by(stcode=row.stockcode).scalar() is not None
            if exists:
                pass
            else:
                logger.info("~~" + row.stockcode + "," + row.stockname + " Not exist")
                obj = Stmaster(stcode=row.stockcode, stname=row.stockname)
                self.session.add(obj)
        self.session.commit()

    def insertDetail(self, thedate, df):
        try:
            for row in df.itertuples():
                stdatum = Stdatum();
                stdatum.stcode = row.stockcode
                stdatum.stdate = thedate
                stdatum.stopen = row.open.replace(',', '')
                stdatum.sthigh = row.high.replace(',', '')
                stdatum.stlow = row.low.replace(',', '')
                stdatum.stclose = row.close.replace(',', '')
                stdatum.stvol = row.volumn.replace(',', '')
                stdatum.stamt = row.amount.replace(',', '')
                self.session.add(stdatum)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # var = traceback.format_exc()
            # Utils().info(traceback.format_exc())
            logger.info(traceback.format_exc())
    #        raise

    def insertQuarterEps(self, stcode, quarter, eps):
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            sql = "INSERT INTO QuarterEps (stcode, quarter,eps) VALUES ('" \
                  + stcode \
                  + "','" \
                  + quarter \
                  + "'," \
                  + eps \
                  + ")"
            print(sql)

            connection.execution_options(autocommit=False).execute(sql)
            # connection.execute(table1.insert(), col1=7, col2='this is some data')
            trans.commit()
        # except:
        #     trans.rollback()
        #     raise
        except Exception as e:
            trans.rollback()
            # var = traceback.format_exc()
            # Utils().info(traceback.format_exc())
            logger.info(traceback.format_exc())
            raise

    # def maintainDetail(self, df, engine):
    #     connection = engine.connect()
    #     trans = connection.begin()
    #     try:
    #         n = 1
    #         for row in df.itertuples():
    #             stdatum=Stdatum();
    #             stdatum.stcode = row.stockcode
    #             stdatum.stopen = row.open.replace(',', '')
    #             stdatum.sthigh = row.high.replace(',', '')
    #             stdatum.stlow = row.low.replace(',', '')
    #             stdatum.stclose = row.close.replace(',', '')
    #             stdatum.stvol = row.volumn.replace(',', '')
    #             stdatum.stamt = row.amount.replace(',', '')
    #
    #             sql = "INSERT INTO T" + stcode + "(thedate, openp,highp,lowp,closep,volumn,amount) VALUES ('" \
    #                   + thedate \
    #                   + "'," \
    #                   + openp \
    #                   + "," \
    #                   + highp \
    #                   + "," \
    #                   + lowp \
    #                   + "," \
    #                   + closep \
    #                   + "," \
    #                   + volumn \
    #                   + "," \
    #                   + amount \
    #                   + ")"
    #             print(str(n) + "  " + sql)
    #             # engine.execute(sql)
    #             n += 1
    #             connection.execution_options(autocommit=False).execute(sql)
    #             # connection.execute(table1.insert(), col1=7, col2='this is some data')
    #         trans.commit()
    #     except:
    #         trans.rollback()
    #         raise
