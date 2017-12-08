'''
    This will read data from Google Spread Sheets and Generate Trade Values.
'''

import os # OS Related
import sys
import json # JSON related
import gspread # Google Spread Sheets

from conf import  constants
from oauth2client.client import SignedJwtAssertionCredentials # Authention related

from Classes import OLHSheetsClass as OLH
import time


def sheets_get_olh_scripts_list(client):
    '''
    This function will get the list of scripts and exchange as dictionary.
    Ex : {'NSE:KTKBANK': 'NSE', 'NSE:VEDL': 'NSE'}
    '''
    # Open WorkBook
    workbook = client.open(constants.INTRA_GOOGLE_SHEET_NAME)
    # Open WorkSheet
    sheet = workbook.worksheet('TECHNICAL')
    #all_cells = SHEET.range('A1:C6')
    #print (all_cells)
    # Read Complete Sheet Data
    sheet_data = sheet.get_all_values()
    olh_scripts = {}

    # Read The Rows.
    # In the sehhet first 3 rows are left blank
    for row in sheet_data[3:]:
        # Read Columns
        # COLUMNS MAPPING
        # A3=>SCRIPT
        # K3 => NSE BUY/SELL
        # L3 => BSE BUY/SELL
        scriptname = row[constants.START]
        if scriptname == '':
            continue
        nse_signal = row[constants.NSE_SIGNAL_INDEX]
        bse_signal = row[constants.BSE_SIGNAL_INDEX]
        if((nse_signal == "SUPER BUY" or nse_signal == "SUPER SELL")
           or (nse_signal == "BUY" and bse_signal == "BUY")
           or (nse_signal == "SELL" and bse_signal == "SELL")):
            exchange = "NSE"

        else:
            exchange = "BSE"
        olh_scripts[scriptname] = exchange
    return olh_scripts
    #print (ALL_CELLS)

def sheets_get_script_data(client,olh_list):
    '''
    This function will read the data for scripts and returns list of IntraSheetsClass objects.

    '''

    # Open WorkBook
    workbook = client.open(constants.INTRA_GOOGLE_SHEET_NAME)
    # Open WorkSheet
    sheet = workbook.worksheet('DATA')
    # Read Complete Sheet Data
    sheet_data = sheet.get_all_values()
    for row in sheet_data[constants.DATA_SKIP_ROWS:]:
        if row[constants.START] in olh_list:
            exchange=olh_list[row[constants.START]]
            if exchange == 'NSE':
                open = row[2]


def sheets_get_olh_data(client):

    '''
    This function will and returns list of OPEN=HIGH or OPEN=LOW OLS SheetsClass objects.

    '''
    # Open WorkBook
    workbook = client.open(constants.INTRA_GOOGLE_SHEET_NAME)
    # Open WorkSheet
    sheet = workbook.worksheet('INTRA_DATA')
    # Read Complete Sheet Data
    sheet_data = sheet.get_all_values()
    olh_data = []
    trade_time = time.strftime(constants.TIME_FORMAT)

    for row in sheet_data[constants.DATA_SKIP_ROWS:]:
        script_name = row[constants.START]
        # Read Nse Data
        nse_open = row[constants.NSE_OPEN_INDEX]
        nse_high = row[constants.NSE_HIGH_INDEX]
        nse_low = row[constants.NSE_LOW_INDEX]
        nse_pclose = row[constants.NSE_PCLOSE_INDEX]
        nse_ltp = row[constants.NSE_LTP_INDEX]
        nse_volume = row[constants.NSE_VOLUME_INDEX]
        #print(script_name,"-",nse_open,nse_high,nse_low,nse_pclose)
        # Read Bse Data
        bse_open = row[constants.BSE_OPEN_INDEX]
        bse_high = row[constants.BSE_HIGH_INDEX]
        bse_low = row[constants.BSE_LOW_INDEX]
        bse_pclose = row[constants.BSE_PCLOSE_INDEX]
        bse_ltp = row[constants.BSE_LTP_INDEX]
        bse_volume = row[constants.BSE_VOLUME_INDEX]
        # Define all conditions as False initially.
        nse_super_buy=False
        nse_super_sell = False
        nse_sell=False
        nse_buy=False

        bse_super_buy=False
        bse_super_sell = False
        bse_sell=False
        bse_buy=False


        # Check NSE OPEN = NSE HIGH = NSE PREVCLOSE
        if nse_open == nse_high == nse_pclose :
            nse_super_sell=True

        # Check NSE OPEN = NSE HIGH
        if nse_open == nse_high != nse_pclose :
            nse_sell=True

        # Check BSE OPEN = BSE HIGH = BSE PREVCLOSE
        if bse_open == bse_high == bse_pclose :
            bse_super_sell=True

        # Check BSE OPEN = BSE HIGH
        if bse_open == bse_high != bse_pclose :
            bse_sell=True

        # Check NSE OPEN = NSE LOW = NSE PREVCLOSE
        if nse_open == nse_low == nse_pclose :
            nse_super_buy=True

        # Check NSE OPEN = NSE LOW
        if nse_open == nse_low != nse_pclose :
            nse_buy=True

        # Check BSE OPEN = BSE LOW = BSE PREVCLOSE
        if bse_open == bse_low == bse_pclose :
            bse_super_buy=True

        # Check BSE OPEN = BSE LOW
        if bse_open == bse_low != bse_pclose :
            bse_buy=True

        oh=False
        ol=False

        cond = None
        p_open = None
        high = None
        low = None
        ltp = None
        pclose = None

        if nse_super_sell & bse_super_sell :
            oh = True
            cond = "NSE-SUPERSELL,BSE-SUPERSELL"
            p_open=nse_open
            high=nse_high
            low=nse_low
            ltp=nse_ltp
            pclose=nse_pclose
        elif nse_super_sell & bse_sell:
            oh = True
            cond = "NSE-SUPERSELL,BSE-SELL"
            p_open=nse_open
            high=nse_high
            low=nse_low
            ltp=nse_ltp
            pclose=nse_pclose
        elif nse_sell & bse_super_sell:
            oh = True
            cond = "NSE-SELL,BSE-SUPERSELL"
            p_open = bse_open
            high = bse_high
            low = bse_low
            ltp = bse_ltp
            pclose = bse_pclose
        elif nse_sell & bse_sell:
            oh = True
            cond = "NSE-SELL,BSE-SELL"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose

        if oh :
            IntraData = OLH.OLHSheetsClass(script_name,trade_time,p_open, high, low, ltp, nse_volume, pclose, cond)
            olh_data.append(IntraData)

        if nse_super_buy & bse_super_buy :
            ol = True
            cond = "NSE-SUPERBUY,BSE-SUPERBUY"
            p_open=nse_open
            high=nse_high
            low=nse_low
            ltp=nse_ltp
            pclose=nse_pclose
        elif nse_super_buy & bse_buy:
            ol = True
            cond = "NSE-SUPERBUY,BSE-BUY"
            p_open=nse_open
            high=nse_high
            low=nse_low
            ltp=nse_ltp
            pclose=nse_pclose
        elif nse_buy & bse_super_buy:
            ol = True
            cond = "NSE-BUY,BSE-SUPERBUY"
            p_open = bse_open
            high = bse_high
            low = bse_low
            ltp = bse_ltp
            pclose = bse_pclose
        elif nse_buy & bse_buy:
            ol = True
            cond = "NSE-BUY,BSE-BUY"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose

        if ol :
            IntraData = OLH.OLHSheetsClass(script_name,trade_time,p_open, high, low, ltp, nse_volume, pclose, cond)
            olh_data.append(IntraData)
    return olh_data

if __name__ == "__main__":
    json_file = sys.argv[1]
    if json_file == None :
        print ("Specify Credential JSON FILE")
        exit(1)
    # Get the base project Dir
    basedir = os.path.dirname(os.getcwd())
    confdir = basedir+os.sep+"conf"
    print ("CONFDIR :",confdir)
    # Credential file
    credentials_file = confdir+ os.sep + json_file

    # Load Credentials
    json_key = json.load(open(credentials_file))
    scope = ['https://spreadsheets.google.com/feeds']
    # Get the Credentials from 'client_email' and 'private_key'
    credentials = SignedJwtAssertionCredentials(json_key['client_email']
                                                , json_key['private_key'].encode()
                                                , scope)
    # Authorize Google Client using Credentials
    client = gspread.authorize(credentials)

    olh_data= sheets_get_olh_data(client)
    print(olh_data)



