from datetime import datetime, date, timedelta, time

import pandas as pd
import pandas_datareader.data as web
import requests
from nsepy import get_history
import json
import numpy
from datetime import datetime,date,timedelta

import pymysql
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Float, Table, Column, ForeignKey, String, BIGINT, DATE
import matplotlib.pyplot as plt
from conf import constants, config
from utils import trade_utils, db_utils




if __name__ == '__main__':
    ALL_SYMBOLS = constants.ALL_SYMBOLS
    TIME_DELTA = 1
    START_DATE = date.today() - timedelta(TIME_DELTA)
    END_DATE = date.today()
    for symbol in ALL_SYMBOLS:
        DF_EOD = trade_utils.get_nse_eoddata(symbol,start_date=START_DATE,end_date=END_DATE)
        #print (DF)
        RESULT_EOD = db_utils.load_db_table(
            symbol
            , DF_EOD
            , config.DB_NAME
            , config.DB_HOST
            , config.DB_USER
            , config.DB_PASSWORD
            , config.DB_EOD_TABLE
        )

        pass


