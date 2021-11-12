import os, sys
from environs import Env
from loguru import logger
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from STModels import Stmaster
from STModels import Stdatum
import traceback

class BASE():
    def __init__(self):
        self.env = Env()
        self.env.read_env(path='.myenv')

        self.DB_PATH=self.env.str('DB_PATH')

        self.FRONT_LOG_FILE = self.env.str('FRONT_LOG_FILE')
        self.LOG_FMT = self.env.str('LOG_FMT')
        logger.remove()
        logger.add(sys.stderr, format=self.LOG_FMT)
        logger.add(self.FRONT_LOG_FILE, format=self.LOG_FMT)

        self.REC_LIMIT = self.env.int('REC_LIMIT')

        self.OLS_SLOPE = self.env.float('OLS_SLOPE')
        self.OLS_DIRECTION = self.env.int('OLS_DIRECTION')

        self.TWSE_CSV_FILE = self.env.str("TWSE_CSV_FILE")