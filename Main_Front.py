#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
from environs import Env
from loguru import logger
from frontend.Mailer import Mailer
from frontend.TWSE import TWSE
from BASE_DB import BASE_DB
# from Utils import Utils
from sqlalchemy import Table
import pandas as pd

# from Mailer import Mailer
from BASE import BASE


class Main_Front(BASE):
    def __init__(self):
        BASE.__init__(self)


        # self.LOG_FMT = self.env.str('LOG_FMT')
        # logger.remove()
        # logger.add(sys.stderr, format=self.LOG_FMT)
        # logger.add(self.FRONT_LOG_FILE, format=self.LOG_FMT)

    def main(self):
        logger.info("************************************************")
        logger.info("Front Start!!!!")


        thedate, df = TWSE().getdata()# get lastest day's data from twse
        logger.info(thedate)

        df = pd.read_csv(self.TWSE_CSV_FILE);
        # logger.info(df)
        # thedate = "2021-01-22"

        db = BASE_DB()
        logger.info("insert Master...")
        db.insertMaster(df)
        logger.info("insert Master done")

        logger.info("insert Detail...")
        db.insertDetail(thedate, df)
        logger.info("insert Detail done")

        logger.info("Mail...")
        Mailer().send()
        logger.info("done")

if __name__ == "__main__":
    Main_Front().main()
