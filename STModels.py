# coding: utf-8
from sqlalchemy import Column, Float, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

#sqlacodegen --outfile c:/mu_py/models.py sqlite:///C:\\mu_py\\mydata.db

t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Stdatum(Base):
    __tablename__ = 'stdata'

    seq = Column(Integer, primary_key=True)
    stcode = Column(Text)
    stdate = Column(Text)
    stopen = Column(Float)
    stclose = Column(Float)
    sthigh = Column(Float)
    stlow = Column(Float)
    stamt = Column(Float)
    stvol = Column(Float)


class Stmaster(Base):
    __tablename__ = 'stmaster'

    myid = Column(Integer, primary_key=True)
    stcode = Column(Text)
    stname = Column(Text)
    ststatus = Column(Text)

class Dividend(Base):
    __tablename__ = 'Dividends'

    seq = Column(Integer, primary_key=True)
    stcode = Column(Text)
    theyear = Column(Integer)
    CashDividend = Column(Float)
    EarningDividend = Column(Float)
    ReserveDividend = Column(Float)
    StockDividend = Column(Float)
    TotalDividend = Column(Float)