'''
    This will contain function used in common.
'''
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Float, Table, Column, \
    ForeignKey, String, BIGINT, DATE, DATETIME, text, exc, select
from conf import constants
import datetime
from conf import config
from utils import db_utils

import pandas as pd

def get_eod_ohlc_data(from_date=datetime.date.today(),to_date=datetime.date.today(),ticker=''):
    '''
        This will get pandas object that contains Open,High,Low,Close,VWAP and volume from eod table for the specified date range.
    :param from_date (start date of the range - inclusive)
    :param from_end (end date of the range - inclusive)
    :return:
        pandas dataset with result of the query
    '''
    if(ticker != ''):
        query = "select ticker, TradeDate, Open, High, Low, Close, VWAP, Volume from {table} where (TradeDate>='{fromdate}' AND TradeDate<='{todate}') AND ticker = '{ticker}'".format(table=config.DB_EOD_TABLE,fromdate=from_date,todate=to_date,ticker=ticker)
    else:
        query = "select ticker, TradeDate, Open, High, Low, Close, VWAP, Volume from {table} where (TradeDate>='{fromdate}' AND TradeDate<='{todate}') ".format(table=config.DB_EOD_TABLE,fromdate=from_date,todate=to_date)
    print("query : ", query)
    ohlc_ds = db_utils.execute_simple_db_query(query, config.DB_NAME,config.DB_HOST, config.DB_USER, config.DB_PASSWORD)
    print (ohlc_ds)


def get_intra_ohlc_5min_data(from_date=datetime.date.today(),start_time=datetime.time(9,15,0),end_time=datetime.time(15,30,0),ticker=''):
    '''
        This will get pandas object that contains Open,High,Low,Close,VWAP and volume from intra 5 min table for the specified date range.
    :param from_date (date for which the intra data to be fetched- default is today date)
    :param start_time (start time of the candle. default - 9:15)
    :param end_time (end time of the candle. )
    : ticker script name.
    :return:
        pandas dataset with result of the query
    '''

    from_time_str = datetime.datetime.combine(from_date,start_time)
    to_time_str = datetime.datetime.combine(from_date, end_time)
    if(ticker != ''):
        query = "select ticker, TradeDate, TradeTime ,Open, High, Low, Close, VWAP, Volume from {table} where TradeDate = '{tradedate}' AND (TradeTime>'{fromtime}' AND TradeTime<='{totime}') AND ticker = '{ticker}'".format(table=config.DB_INTRA_5MIN_TABLE,tradedate=from_date,fromtime=from_time_str,totime=to_time_str,ticker=ticker)
    else:
        query = "select ticker, TradeDate, TradeTime ,Open, High, Low, Close, VWAP, Volume from {table} where TradeDate = '{tradedate}' AND (TradeTime>'{fromtime}' AND TradeTime<='{totime}')".format(
            table=config.DB_INTRA_5MIN_TABLE, tradedate=from_date, fromtime=from_time_str, totime=to_time_str)
    print("query : ", query)
    intra_ohlc_ds = db_utils.execute_simple_db_query(query, config.DB_NAME,config.DB_HOST, config.DB_USER, config.DB_PASSWORD)
    df = pd.DataFrame(intra_ohlc_ds['result'],
                      columns=['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Vwap', 'Volume'])
    return df
    #print (intra_ohlc_ds)

def get_intra_ohlc_15min_data(from_date=datetime.date.today(),start_time=datetime.time(9,15,0),end_time=datetime.time(15,30,0),ticker=''):
    '''
        This will get pandas object that contains Open,High,Low,Close,VWAP and volume from intra 15 min table for the specified date range.
    :param from_date (date for which the intra data to be fetched- default is today date)
    :param start_time (start time of the candle. default - 9:15)
    :param end_time (end time of the candle. )
    : ticker script name.
    :return:
        pandas dataset with result of the query
    '''

    from_time_str = datetime.datetime.combine(from_date,start_time)
    to_time_str = datetime.datetime.combine(from_date, end_time)
    if(ticker != ''):
        query = "select ticker, TradeDate, TradeTime ,Open, High, Low, Close, VWAP, Volume from {table} where TradeDate = '{tradedate}' AND (TradeTime>'{fromtime}' AND TradeTime<='{totime}') AND ticker = '{ticker}'".format(table=config.DB_INTRA_15MIN_TABLE,tradedate=from_date,fromtime=from_time_str,totime=to_time_str,ticker=ticker)
    else:
        query = "select ticker, TradeDate, TradeTime ,Open, High, Low, Close, VWAP, Volume from {table} where TradeDate = '{tradedate}' AND (TradeTime>'{fromtime}' AND TradeTime<='{totime}')".format(
            table=config.DB_INTRA_15MIN_TABLE, tradedate=from_date, fromtime=from_time_str, totime=to_time_str)
    print("query : ", query)
    intra_ohlc_ds = db_utils.execute_simple_db_query(query, config.DB_NAME,config.DB_HOST, config.DB_USER, config.DB_PASSWORD)
    df = pd.DataFrame(intra_ohlc_ds['result'],
                      columns=['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Vwap', 'Volume'])
    return df

    #print (intra_ohlc_ds)



def get_intra_ohlc_first_15min_candle(from_date=datetime.date.today(),ticker=''):
    '''
        This will give the first 15 min candle information
    :param from_date (date for which the intra data to be fetched- default is today date)
    : ticker script name.
    :return:
        pandas dataset with result of the query
    '''
    return get_intra_ohlc_15min_data(from_date=from_date,ticker=ticker,end_time=datetime.time(9,30,0))

def get_intra_ohlc_first_30min_candle(from_date=datetime.date.today(),ticker=''):
    '''
        This will give the first 30 min candle information
    :param from_date (date for which the intra data to be fetched- default is today date)
    : ticker script name.
    :return:
        pandas dataset with result of the query
    '''
    return get_intra_ohlc_15min_data(from_date=from_date,ticker=ticker,end_time=datetime.time(9,30,0))
