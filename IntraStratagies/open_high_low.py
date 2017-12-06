'''
    This will read data from Google Spread Sheets and Generate Trade Values.
'''

import os # OS Related
import math
import sys
import json # JSON related
import gspread # Google Spread Sheets

from oauth2client.client import SignedJwtAssertionCredentials # Authention related

from Classes import OLHSheetsClass as olh
from Classes import OLHTradeClass as olht

from conf import constants
from utils import trade_utils


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
    for row in sheet_data[constants.DATA_SKIP_ROWS:]:
        script_name = row[constants.START]
        # Read Nse Data
        nse_open = row[constants.NSE_OPEN_INDEX]
        nse_high = row[constants.NSE_HIGH_INDEX]
        nse_low = row[constants.NSE_LOW_INDEX]
        nse_pclose = row[constants.NSE_PCLOSE_INDEX]
        nse_ltp = row[constants.NSE_LTP_INDEX]
        #print(script_name,"-",nse_open,nse_high,nse_low,nse_pclose)
        # Read Bse Data
        bse_open = row[constants.BSE_OPEN_INDEX]
        bse_high = row[constants.BSE_HIGH_INDEX]
        bse_low = row[constants.BSE_LOW_INDEX]
        bse_pclose = row[constants.BSE_PCLOSE_INDEX]
        bse_ltp = row[constants.BSE_LTP_INDEX]
        # Define all conditions as False initially.
        nse_super_buy = False
        nse_super_sell = False
        nse_sell = False
        nse_buy = False

        bse_super_buy = False
        bse_super_sell = False
        bse_sell = False
        bse_buy = False


        # Check NSE OPEN = NSE HIGH = NSE PREVCLOSE
        if nse_open == nse_high == nse_pclose:
            nse_super_sell = True

        # Check NSE OPEN = NSE HIGH
        if nse_open == nse_high != nse_pclose:
            nse_sell = True

        # Check BSE OPEN = BSE HIGH = BSE PREVCLOSE
        if bse_open == bse_high == bse_pclose:
            bse_super_sell = True

        # Check BSE OPEN = BSE HIGH
        if bse_open == bse_high != bse_pclose:
            bse_sell = True

        # Check NSE OPEN = NSE LOW = NSE PREVCLOSE
        if nse_open == nse_low == nse_pclose:
            nse_super_buy = True

        # Check NSE OPEN = NSE LOW
        if nse_open == nse_low != nse_pclose:
            nse_buy = True

        # Check BSE OPEN = BSE LOW = BSE PREVCLOSE
        if bse_open == bse_low == bse_pclose:
            bse_super_buy = True

        # Check BSE OPEN = BSE LOW
        if bse_open == bse_low != bse_pclose:
            bse_buy = True

        open_high = False
        open_low = False

        cond = None
        p_open = None
        high = None
        low = None
        ltp = None
        pclose = None

        if nse_super_sell & bse_super_sell:
            open_high = True
            cond = "NSE-SUPERSELL,BSE-SUPERSELL"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose
        elif nse_super_sell & bse_sell:
            open_high = True
            cond = "NSE-SUPERSELL,BSE-SELL"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose
        elif nse_sell & bse_super_sell:
            open_high = True
            cond = "NSE-SELL,BSE-SUPERSELL"
            p_open = bse_open
            high = bse_high
            low = bse_low
            ltp = bse_ltp
            pclose = bse_pclose
        elif nse_sell & bse_sell:
            open_high = True
            cond = "NSE-SELL,BSE-SELL"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose

        if open_high:
            intra_data = olh.OLHSheetsClass(script_name, float(p_open)
                                            , float(high), float(low)
                                            , float(ltp), float(pclose), cond)
            olh_data.append(intra_data)

        if nse_super_buy & bse_super_buy:
            open_low = True
            cond = "NSE-SUPERBUY,BSE-SUPERBUY"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose
        elif nse_super_buy & bse_buy:
            open_low = True
            cond = "NSE-SUPERBUY,BSE-BUY"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose
        elif nse_buy & bse_super_buy:
            open_low = True
            cond = "NSE-BUY,BSE-SUPERBUY"
            p_open = bse_open
            high = bse_high
            low = bse_low
            ltp = bse_ltp
            pclose = bse_pclose
        elif nse_buy & bse_buy:
            open_low = True
            cond = "NSE-BUY,BSE-BUY"
            p_open = nse_open
            high = nse_high
            low = nse_low
            ltp = nse_ltp
            pclose = nse_pclose

        if open_low:
            intra_data = olh.OLHSheetsClass(script_name, float(p_open)
                                            , float(high), float(low)
                                            , float(ltp), float(pclose), cond)
            olh_data.append(intra_data)
    return olh_data


def sheets_generate_olh_trade_data(intra_stocks_list):
    '''
    This will Generate Trade Data for Open=High/Low Strategy
    :param intra_stocks_list:
    :return: list of OLHTTradeClass objects
    '''
    olh_trade_list = []
    for olh_script in intra_stocks_list:
        script = olh_script.script
        open_price = olh_script.p_open
        high_price = olh_script.high
        low_price = olh_script.low
        prev_close = olh_script.pclose
        cmp = olh_script.ltp
        cond = olh_script.cond
        atp = (high_price + low_price) / 2
        pivot = (prev_close + open_price + atp) / 3
        if olh_script.cond.find(constants.BUY_STRING) != constants.STR_NOT_FOUND_VALUE:
            trade_string = cond+"_BUY ABOVE"
            gann_values = trade_utils.generate_gann_square(open_price)
            gann_targets_list = [price for price in gann_values if price > open_price]
            stop_loss = gann_values[gann_values.index(gann_targets_list[0]) - 1]
            gann_targets_list[1:] = [round(price * constants.RESISTANCE_FILTER
                                           , constants.NUM_DECIMAL_PLACES)
                                     for price in gann_targets_list[1:6]]
            buy_level1 = int(round((math.sqrt(open_price) - 0.02) ** 2, 0))
            buy_level2 = int(round((math.sqrt(open_price) + 0.0833) ** 2, 0))
            buy_level3 = int(round((math.sqrt(open_price) + 0.285) ** 2, 0))
            buysl = round((min(buy_level1, stop_loss) -
                           (min(buy_level1, stop_loss) * constants.BUY_SL_FILTER)),
                          constants.NUM_DECIMAL_PLACES)
            # Bonus Buy
            entry3 = round(stop_loss * constants.BUY_ENTRY3_FILTER, constants.NUM_DECIMAL_PLACES)
            # Buy If Green
            entry2 = min(buy_level2, gann_targets_list[0])
            # Hold If Green
            entry1 = max(buy_level2, gann_targets_list[0])
            # target1
            target1 = gann_targets_list[1]
            # target2
            target2 = max(buy_level3, gann_targets_list[2])
            # EXTENDED target3
            target3 = gann_targets_list[3]
            # EXTENDED target4
            target4 = gann_targets_list[4]
            # EXTENDED target5
            target5 = gann_targets_list[5]
            olh_trade_class = olht.OLHTradeClass(script,open_price, high_price,low_price,cmp, prev_close
                                                 , pivot, atp, trade_string
                                                 , buysl, entry1, entry2, entry3
                                                 , target1, target2, target3
                                                 , target4, target5)
            olh_trade_list.append(olh_trade_class)
        elif olh_script.cond.find(constants.SELL_STRING) != constants.STR_NOT_FOUND_VALUE:
            trade_string = cond+"_SELL BELOW"
            gann_values = trade_utils.generate_gann_square(open_price)
            gann_values = gann_values[::-1]
            gann_targets_list = [price for price in gann_values if price < open_price]
            stop_loss = gann_values[gann_values.index(gann_targets_list[0]) - 1]
            gann_targets_list[1:] = [round(price * constants.SUPPORT_FILTER
                                           , constants.NUM_DECIMAL_PLACES) for price in
                                     gann_targets_list[1:6]]
            sell_level1 = int(round((math.sqrt(open_price) + 0.02) ** 2, 0))
            sell_level2 = int(round((math.sqrt(open_price) - 0.0833) ** 2, 0))
            sell_level3 = int(round((math.sqrt(open_price) - 0.285) ** 2, 0))
            sellsl = round((max(sell_level1, stop_loss) +
                            (max(sell_level1, stop_loss) * constants.SELL_SL_FILTER)),
                           constants.NUM_DECIMAL_PLACES)
            # Bonus Sell
            entry3 = round(stop_loss * constants.SELL_ENTRY3_FILTER, constants.NUM_DECIMAL_PLACES)
            # Short If Red
            entry2 = max(sell_level2, gann_targets_list[0])
            # Hold If Red
            entry1 = min(sell_level2, gann_targets_list[0])
            # target1
            target1 = gann_targets_list[1]
            # target2
            target2 = min(sell_level3, gann_targets_list[2])
            # EXTENDED target3
            target3 = gann_targets_list[3]
            # EXTENDED target4
            target4 = gann_targets_list[4]
            # EXTENDED target5
            target5 = gann_targets_list[5]
            olh_trade_class = olht.OLHTradeClass(script, open_price, high_price, low_price, cmp, prev_close, pivot, atp
                                                 , trade_string, sellsl, entry1
                                                 , entry2, entry3, target1, target2
                                                 , target3, target4, target5)
            olh_trade_list.append(olh_trade_class)
    return olh_trade_list

if __name__ == "__main__":
    JSON_FILE = sys.argv[1]
    if JSON_FILE is None:
        print("Specify Credential JSON FILE")
        exit(1)
    # Get the base project Dir
    BASEDIR = os.path.dirname(os.getcwd())
    CONFDIR = BASEDIR+os.sep+"conf"
    print("CONFDIR :", CONFDIR)
    # Credential file
    CREDENTIALS_FILE = CONFDIR+ os.sep + JSON_FILE

    # Load Credentials
    JSON_KEY = json.load(open(CREDENTIALS_FILE))
    SCOPE = ['https://spreadsheets.google.com/feeds']
    # Get the Credentials from 'client_email' and 'private_key'
    CREDENTIALS = SignedJwtAssertionCredentials(JSON_KEY['client_email']
                                                , JSON_KEY['private_key'].encode()
                                                , SCOPE)
    # Authorize Google Client using Credentials
    CLIENT = gspread.authorize(CREDENTIALS)

    OLH_DATA = sheets_get_olh_data(CLIENT)
    print(OLH_DATA)



