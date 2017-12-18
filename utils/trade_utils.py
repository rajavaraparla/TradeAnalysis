'''
    This will contain required functions/utilities used by all  modules
'''
import math
import os
import re
import fpdf
import csv
import pandas as pd
import requests
import datetime
# SMTP Library used for SendMail
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


import time
from conf import constants, config
from nsepy import get_history
from utils import db_utils
import pymysql
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Float, Table, Column, ForeignKey, String, BIGINT, DATE, DATETIME


from Templates import open_high_low_templ
import xlsxwriter as xlsx

def generate_gann_square(price):
    ''' This will give list of all Gann Values for the specified stock value '''
    sqrt_price = int(math.sqrt(price)-1)
    gann_square = [round((sqrt_price+gann_quot)**2, constants.NUM_DECIMAL_PLACES)
                   for gann_quot in constants.GANN_QUOTIENTS]
    return gann_square


def generate_pdf_olh_intra(olh_trade_class_list, pdf_file_name):
    '''
    This will create pdf file
    :param olh_trade_class_list:
    :param pdf_file_name:
    :return:
    '''
    pdf_fh = fpdf.FPDF()
    pdf_fh.add_page()
    pdf_header_string = constants.HEADER_OPEN_HIGH_LOW
    pdf_fh.set_font('Courier', size=9)
    pdf_fh.write(5, txt=pdf_header_string)

    for index,olh_trade_class in enumerate(olh_trade_class_list):

        pdf_string = ''
        pdf_fh.add_page()
        if olh_trade_class.trade_str.find(constants.SELL_STRING) != constants.STR_NOT_FOUND_VALUE:
            pdf_fh.set_font('Courier',size=7)
            oh_string = open_high_low_templ.OH_STRING
            oh_string = str(index+1)+" . "+oh_string
            pdf_fh.set_text_color(255,0,0)
            #print(oh_string)
            oh_string = oh_string.replace('#SCRIPT#', str(olh_trade_class.script))
            oh_string = oh_string.replace('#CMP#', str(olh_trade_class.ltp))

            if olh_trade_class.ltp < olh_trade_class.atp:
                oh_string = oh_string.replace('#TRADE_ATP#', "YES")
            else:
                oh_string = oh_string.replace('#TRADE_ATP#', "NO")

            if olh_trade_class.ltp < olh_trade_class.ipivot:
                oh_string = oh_string.replace('#TRADE_PIVOT#', "YES")
            else:
                oh_string = oh_string.replace('#TRADE_PIVOT#', "NO")

            if olh_trade_class.ltp < olh_trade_class.pclose:
                oh_string = oh_string.replace('#TRADE_PCLOSE#', "YES")
            else:
                oh_string = oh_string.replace('#TRADE_PCLOSE#', "NO")

            oh_string = oh_string.replace('#SL#', str(olh_trade_class.sl))
            oh_string = oh_string.replace('#ENTRY3#', str(olh_trade_class.entry3))
            oh_string = oh_string.replace('#ENTRY2#', str(olh_trade_class.entry2))
            oh_string = oh_string.replace('#ENTRY1#', str(olh_trade_class.entry1))

            oh_string = oh_string.replace('#TARGET1#', str(olh_trade_class.target1))
            oh_string = oh_string.replace('#TARGET2#', str(olh_trade_class.target2))
            oh_string = oh_string.replace('#TARGET3#', str(olh_trade_class.target3))
            oh_string = oh_string.replace('#TARGET4#', str(olh_trade_class.target4))
            oh_string = oh_string.replace('#TARGET5#', str(olh_trade_class.target5))

            oh_string = oh_string.replace('#LOW_MADE#', str(olh_trade_class.low))

            reg_exp = re.compile(constants.NSE_STRING+"-(.*?),")
            nse_signal = reg_exp.search(olh_trade_class.trade_str)
            #print ("NSE_SIGNAL",nse_signal.groups()[0])

            reg_exp = re.compile(constants.BSE_STRING + "-(.*?)_")
            bse_signal = reg_exp.search(olh_trade_class.trade_str)
            #print ("BSE_SIGNAL",bse_signal.groups()[0])
            oh_string = oh_string.replace('#NSE_SIGNAL#', nse_signal.groups()[0])
            oh_string = oh_string.replace('#BSE_SIGNAL#', bse_signal.groups()[0])
            pdf_string = oh_string
        elif olh_trade_class.trade_str.find(constants.BUY_STRING) != constants.STR_NOT_FOUND_VALUE :
            pdf_fh.set_font('Courier',size=7)
            ol_string = open_high_low_templ.OL_STRING
            ol_string = str(index+1) + " . "+ol_string
            pdf_fh.set_text_color(0,0,255)
            ol_string = ol_string.replace('#SCRIPT#', str(olh_trade_class.script))
            ol_string = ol_string.replace('#CMP#', str(olh_trade_class.ltp))

            if olh_trade_class.ltp > olh_trade_class.atp:
                ol_string = ol_string.replace('#TRADE_ATP#', "YES")
            else:
                ol_string = ol_string.replace('#TRADE_ATP#', "NO")

            if olh_trade_class.ltp > olh_trade_class.ipivot:
                ol_string = ol_string.replace('#TRADE_PIVOT#', "YES")
            else:
                ol_string = ol_string.replace('#TRADE_PIVOT#', "NO")

            if olh_trade_class.ltp > olh_trade_class.pclose:
                ol_string = ol_string.replace('#TRADE_PCLOSE#', "YES")
            else:
                ol_string = ol_string.replace('#TRADE_PCLOSE#', "NO")

            ol_string = ol_string.replace('#SL#', str(olh_trade_class.sl))
            ol_string = ol_string.replace('#ENTRY3#', str(olh_trade_class.entry3))
            ol_string = ol_string.replace('#ENTRY2#', str(olh_trade_class.entry2))
            ol_string = ol_string.replace('#ENTRY1#', str(olh_trade_class.entry1))

            ol_string = ol_string.replace('#TARGET1#', str(olh_trade_class.target1))
            ol_string = ol_string.replace('#TARGET2#', str(olh_trade_class.target2))
            ol_string = ol_string.replace('#TARGET3#', str(olh_trade_class.target3))
            ol_string = ol_string.replace('#TARGET4#', str(olh_trade_class.target4))
            ol_string = ol_string.replace('#TARGET5#', str(olh_trade_class.target5))

            ol_string = ol_string.replace('#HIGH_MADE#', str(olh_trade_class.high))

            reg_exp = re.compile(constants.NSE_STRING + "-(.*?),")
            nse_signal = reg_exp.search(olh_trade_class.trade_str)
            #print("NSE_SIGNAL", nse_signal.groups()[0])

            reg_exp = re.compile(constants.BSE_STRING + "-(.*?)_")
            bse_signal = reg_exp.search(olh_trade_class.trade_str)
            #print("BSE_SIGNAL", bse_signal.groups()[0])
            ol_string = ol_string.replace('#NSE_SIGNAL#', nse_signal.groups()[0])
            ol_string = ol_string.replace('#BSE_SIGNAL#', bse_signal.groups()[0])
            pdf_string = ol_string

        #pdf_fh.text(x=10,y=20,txt = oh_string)
        pdf_fh.write(5, txt = pdf_string)

    pdf_fh.output(pdf_file_name, "F")


def generate_excel_olh_intra(olh_trade_class_list,xls_file_name):
    '''
    This will create pdf file
    :param olh_trade_class_list:
    :param pdf_file_name:
    :return:
    '''
    columns = [
                  'SCRIPT', 'NSE', 'BSE', 'TRADE'
               , 'ENTRY1','ENTRY2', 'ENTRY3', 'SL'
               , 'TARGET1', 'TARGET2', 'TARGET3'
               , 'TARGET4', 'TARGET5'
    ]
    workbook = xlsx.Workbook(xls_file_name)
    format_blue = workbook.add_format({'bold': True, 'font_color': 'blue'})
    format_red = workbook.add_format({'font_color': 'red'})
    format_green = workbook.add_format({'font_color': 'green'})

    worksheet = workbook.add_worksheet('Open=High-Low')
    for index,column in enumerate(columns):
        worksheet.write(constants.START+constants.ROWS_SKIP, index, column,format_blue)
    for index,olh_trade_class in enumerate(olh_trade_class_list):
        if olh_trade_class.trade_str.find(constants.SELL_STRING) != constants.STR_NOT_FOUND_VALUE:
            pass
        elif olh_trade_class.trade_str.find(constants.BUY_STRING) != constants.STR_NOT_FOUND_VALUE:
            pass

    workbook.close()

def get_intra_5min_data(ticker,days=1):
    '''
    extract data in 15 min candles
    :param ticker:
    :param days:
    :return: a data frame of 15 min data.
    '''
    return get_google_finance_intraday(ticker, period=300, days=days)


def get_intra_15min_data(ticker,days=1):
    '''
    extract data in 15 min candles
    :param ticker:
    :param days:
    :return: a data frame of 15 min data.
    '''
    return get_google_finance_intraday(ticker, period=900, days=days)

def get_intra_30min_data(ticker, days=1):
    '''
    extract data in 30 min candles
    :param ticker:
    :param days:
    :return: a data frame of 15 min data.
    '''

    return get_google_finance_intraday(ticker, period=1800, days=days)

def get_intra_hour_data(ticker, days=1):
    '''
    extract data in 60 min candles
    :param ticker:
    :param days:
    :return: a data frame of 15 min data.
    '''
    return get_google_finance_intraday(ticker, period=3600, days=days)


def get_google_finance_intraday(ticker, period=60, days=1,exchange="NSE"):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    uri = "https://finance.google.com/finance/getprices?p={days}d&i={period}&f=d,o,h,l,c,v&q={ticker}&x={exch}".format(
        days=days, period=period, ticker=ticker,exch=exchange)
    response = requests.get(url=uri)
    # print(type(response))
    # print (type(response.content))
    # print (response.text)
    #
    reader = csv.reader((response.content.decode("utf-8")).splitlines())
    #print(type(reader))
    rows = []
    columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    times = []
    # Skip first 7 rows as it contains header info
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))

    if len(rows):
        df = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='TTime'), columns=columns)
        df['TradeTime'] = df.index
        df['ticker'] = ticker
        df['TradeDate'] = df['TradeTime'].dt.date
        return df
    else:
        df = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='TTime'), columns=columns)
        df['TradeTime'] = df.index
        df['ticker'] = ticker
        df['TradeDate'] = df['TradeTime'].dt.date
        return df



def get_nse_eoddata(ticker, start_date=datetime.date.today(), end_date=datetime.timedelta(1)):
    """
    Retrieve  EOD stock data from NSE.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    start_date: date object
        Start Date
    end_date : date object
        End Date.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing :
            Ticekr,
            TradeDate,
            Open,
            High,
            Low,
            Close,
            VWAP,
            Volume,
            Deliverable Volume,
            Percentage Deliverables
    """

    df = get_history(symbol=ticker, start=start_date, end=end_date)

    df = df.drop('Prev Close', 1)
    df = df.drop('Last', 1)
    df = df.drop('Series', 1)
    df = df.drop('Turnover', 1)
    df = df.drop('Trades', 1)


    df['TradeDate'] = pd.to_datetime(df.index, errors='coerce')

    #df['TradeDate'] = (df.index).dt.date
    df = df.rename(columns={'Symbol': 'ticker', '%Deliverble': 'Percentage_Deliverables','Deliverable Volume':'Deliverable_Volume'})
    df = df.set_index('TradeDate', 'ticker')
    df['TradeDate'] = df.index
    #print(df.head())
    return df


def sendMail(fileName):
    '''
        Send email
    :param recipent_list:
    :param fileName:
    :return:
    '''
    recipients = constants.MAIL_TO
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    subject = "OLH for "+time.strftime(constants.TIME_FORMAT)
    msg['Subject'] = subject
    msg['From'] = config.MAIL_USERNAME_FROM
    msg.preamble = 'Multipart massage.\n'

    part = MIMEText("Hi, please find the attached file")
    msg.attach(part)

    part = MIMEApplication(open(fileName, "rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=fileName)
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.ehlo()
    server.starttls()
    server.login(config.MAIL_USERNAME_FROM, config.MAIL_PASSWORD_FROM)

    server.sendmail(msg['From'], emaillist, msg.as_string())
    server.close()
    pass


def insert_olh_intra_trade_db(olh_trade_class_list, tablename, dbname, dbhost, dbuser, dbpassword):
    '''
    This will load the intra trade database with the qualified trades for the day
    :param olh_trade_class_list:
    :param tablename:
    :param dbname:
    :param dbhost:
    :param dbuser:
    :param dbpassword:
    :return SUCCESS/FAILURE:
    '''
    for index,olh_trade_class in enumerate(olh_trade_class_list):
        script = olh_trade_class.script
        cmp = olh_trade_class.ltp
        atp = olh_trade_class.atp
        ipivot = olh_trade_class.ipivot
        pclose = olh_trade_class.pclose
        sl = olh_trade_class.sl
        entry1 = olh_trade_class.entry1
        entry2 = olh_trade_class.entry2
        entry3 = olh_trade_class.entry3
        target1 = olh_trade_class.target1
        target2 = olh_trade_class.target2
        target3 = olh_trade_class.target3
        target4 = olh_trade_class.target4
        target5 = olh_trade_class.target5
        high = olh_trade_class.high
        low = olh_trade_class.low
        open = None
        if olh_trade_class.trade_str.find(constants.SELL_STRING) != constants.STR_NOT_FOUND_VALUE:
            open = olh_trade_class.high
        elif olh_trade_class.trade_str.find(constants.BUY_STRING) != constants.STR_NOT_FOUND_VALUE :
            open = olh_trade_class.low
        tradedate = datetime.date.today().strftime(constants.DATE_FORMAT)
        tradetime = time.strftime(constants.TIME_FORMAT)
        reg_exp = re.compile(constants.NSE_STRING + "-(.*?),")
        nsesignal = reg_exp.search(olh_trade_class.trade_str)
        reg_exp = re.compile(constants.BSE_STRING + "-(.*?)_")
        bsesignal = reg_exp.search(olh_trade_class.trade_str)
        params_dict = {}
        params_dict[constants.INTRA_OLH_TRADE_TICKER] = script
        params_dict[constants.INTRA_OLH_TRADE_CLOSE] = cmp
        params_dict[constants.INTRA_OLH_TRADE_PCLOSE] = pclose
        params_dict[constants.INTRA_OLH_TRADE_OPEN] = open
        params_dict[constants.INTRA_OLH_TRADE_HIGH] = high
        params_dict[constants.INTRA_OLH_TRADE_LOW] = low
        params_dict[constants.INTRA_OLH_TRADE_IPIVOT] = ipivot
        params_dict[constants.INTRA_OLH_TRADE_ATP] = atp
        params_dict[constants.INTRA_OLH_TRADE_NSE_TRADE] = nsesignal
        params_dict[constants.INTRA_OLH_TRADE_BSE_TRADE] = bsesignal
        params_dict[constants.INTRA_OLH_TRADE_ENTRY1] = entry1
        params_dict[constants.INTRA_OLH_TRADE_ENTRY2] = entry2
        params_dict[constants.INTRA_OLH_TRADE_ENTRY3] = entry3
        params_dict[constants.INTRA_OLH_TRADE_SL] = sl
        params_dict[constants.INTRA_OLH_TRADE_TARGET1] = target1
        params_dict[constants.INTRA_OLH_TRADE_TARGET2] = target2
        params_dict[constants.INTRA_OLH_TRADE_TARGET3] = target3
        params_dict[constants.INTRA_OLH_TRADE_TARGET4] = target4
        params_dict[constants.INTRA_OLH_TRADE_TARGET5] = target5
        params_dict[constants.INTRA_OLH_TRADE_TRADE_DATE] = tradedate
        params_dict[constants.INTRA_OLH_TRADE_TRADE_TIME] = tradetime

        insert_status = db_utils.execute_insert_query(tablename = config.DB_INTRA_OLH_TRADE_TABLENAME
                                                      , dbname = dbname
                                                      , dbhost = dbhost
                                                      , dbpassword = dbpassword
                                                      , dbuser = dbuser
                                                      , params = params_dict)
        return insert_status






