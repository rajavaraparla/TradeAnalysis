from datetime import datetime, date, timedelta, time

import pandas as pd
import pandas_datareader.data as web
import requests
# from nsepy.archives import get_price_history
from nsepy import get_history
import json
import numpy

import pymysql
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Float, Table, Column, ForeignKey, String, BIGINT, DATE
import matplotlib.pyplot as plt

startDate = date.today() - timedelta(days=1)
# Use this if you are running same day
endDate = date.today()

allsymbols = ['ACC', 'ADANIENT', 'ADANIPORTS', 'ADANIPOWER', 'ABIRLANUVO', 'AJANTPHARM', 'ALBK', 'AMARAJABAT',
              'AMBUJACEM', 'ANDHRABANK', 'APOLLOHOSP', 'APOLLOTYRE', 'ARVIND', 'ASHOKLEY', 'ASIANPAINT', 'AUROPHARMA',
              'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BANKBARODA', 'BANKINDIA', 'BATAINDIA', 'BEML', 'BEL',
              'BHARATFIN', 'BHARATFORG', 'BHEL', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BIOCON', 'BOSCHLTD', 'BRITANNIA',
              'CADILAHC', 'CAIRN', 'CANBK', 'CASTROLIND', 'CEATLTD', 'CENTURYTEX', 'CESC', 'CIPLA', 'COALINDIA',
              'COLPAL', 'CONCOR', 'CROMPGREAV', 'CUMMINSIND', 'DABUR', 'DHFL', 'DISHTV', 'DIVISLAB', 'DLF', 'DRREDDY',
              'EICHERMOT', 'ENGINERSIN', 'EXIDEIND', 'GAIL', 'GLENMARK', 'GMRINFRA', 'GODREJCP', 'GODREJIND',
              'GRANULES', 'GRASIM', 'HAVELLS', 'HCLTECH', 'HDFCBANK', 'HEROMOTOCO', 'HEXAWARE', 'HINDALCO', 'HINDPETRO',
              'HINDUNILVR', 'HINDZINC', 'HDIL', 'HDFC', 'ICICIBANK', 'IDBI', 'IDEA', 'IDFC', 'IFCI', 'IBULHSGFIN',
              'IBREALEST', 'IOC', 'ICIL', 'IGL', 'INDUSINDBK', 'INFY', 'IRB', 'ITC', 'JISLJALEQS', 'JPASSOCIAT',
              'JETAIRWAYS', 'JINDALSTEL', 'JSWENERGY', 'JSWSTEEL', 'JUBLFOOD', 'JUSTDIAL', 'KSCL', 'KOTAKBANK', 'KPIT',
              'LT', 'LICHSGFIN', 'LUPIN', 'MARICO', 'MARUTI', 'MCLEODRUSS', 'MINDTREE', 'MOTHERSUMI', 'MRF', 'NCC',
              'NHPC', 'NIITTECH', 'NMDC', 'NTPC', 'ONGC', 'OIL', 'OFSS', 'ORIENTBANK', 'PAGEIND', 'PCJEWELLER',
              'PETRONET', 'PIDILITIND', 'PFC', 'POWERGRID', 'PTC', 'PNB', 'RELCAPITAL', 'RCOM', 'RELIANCE', 'RELINFRA',
              'RPOWER', 'RECLTD', 'SRTRANSFIN', 'SIEMENS', 'SINTEX', 'SRF', 'SBIN', 'SAIL', 'STAR', 'SUNPHARMA',
              'SUNTV', 'SYNDIBANK', 'TATACHEM', 'TATACOMM', 'TCS', 'TATAELXSI', 'TATAGLOBAL', 'TATAMOTORS',
              'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'FEDERALBNK', 'INDIACEM', 'KTKBANK', 'SOUTHBANK',
              'TITAN', 'TORNTPHARM', 'TV18BRDCST', 'TVSMOTOR', 'ULTRACEMCO', 'UNIONBANK', 'UNITECH', 'UBL',
              'MCDOWELL-N', 'UPL', 'VEDL', 'VOLTAS', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL']
allsymbols = ['MARUTI']

# allsymbols = ['TATAPOWER', 'TATASTEEL', 'TECHM', 'FEDERALBNK', 'INDIACEM', 'KTKBANK', 'SOUTHBANK', 'TITAN', 'TORNTPHARM', 'TV18BRDCST', 'TVSMOTOR', 'ULTRACEMCO', 'UNIONBANK', 'UNITECH', 'UBL', 'MCDOWELL-N', 'UPL', 'VEDL', 'VOLTAS', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL']

for symbol in allsymbols:
    print("downloading Symbol %s For Date %s" % (symbol, endDate))
    # S1 = get_price_history(stock=symbol, start=startDate, end=endDate)
    S1 = get_history(symbol=symbol, start=startDate, end=endDate)
    S1 = S1.drop('Prev Close', 1)
    S1 = S1.drop('Last', 1)
    S1 = S1.drop('Series', 1)
    S1 = S1.drop('Turnover', 1)
    S1 = S1.drop('Trades', 1)
    # S1.index.name = 'Date'
    S1['TradeDate'] = S1.index

    # S1['VWAPAvg']=pd.rolling_mean(S1["VWAP"],20)

    # plt.plot(S1["TradeDate"],S1["VWAP"], label='VWAP')
    #     plt.plot(S1["TradeDate"],S1["Close"], label='Close')
    #
    #     plt.plot(S1["TradeDate"],S1["VWAPAvg"], marker='o', linestyle='--', color='r', label='VWAPAvg')
    #     plt.xlabel('Radius/Side')
    #     plt.ylabel('Area')
    #     plt.title('Area of Shapes')
    #     plt.legend()
    #     plt.show()
    S1['TradeDate'] = pd.to_datetime(S1['TradeDate'], errors='coerce')
    # S1['TradeDate'] = S1['TradeDate'].dt.date
    S1 = S1.rename(columns={'Symbol': 'ticker', '%Deliverble': 'Percentage Deliverables'})

    S1 = S1.set_index('TradeDate', 'ticker')

    print(S1.columns)
    print(S1)

    # print(S1)

    engine = create_engine('mysql+pymysql://' + 'taadmin:Progress!2009@localhost/tradedata')
    meta = MetaData(bind=engine)
    ## ACTOR PARROT TABLE ###
    table_hist_data = Table('hist_data', meta,
                            Column('ticker', String(255), primary_key=True, nullable=False),
                            Column('TradeDate', DATE, primary_key=True, nullable=False),
                            Column('Open', Float, nullable=False),
                            Column('High', Float, nullable=False),
                            Column('Low', Float, nullable=False),
                            Column('Close', Float, nullable=False),
                            Column('VWAP', Float, nullable=False),
                            Column('Volume', BIGINT, nullable=False),
                            Column('Deliverable Volume', BIGINT, nullable=False),
                            Column('Percentage Deliverables', Float, nullable=False)
                            )

    meta.create_all(engine)
    print("loading Symbol %s" % (symbol))
    S1.to_sql('hist_data', engine, flavor='mysql', chunksize=1000, if_exists='append', index=True)
