'''
    This will read data from Google Spread Sheets and Generate Trade Plan.
    This is Open=High/ Open=Low Strategy
'''

import os  # OS Related
import json  # JSON related
import time
import datetime
import gspread  # Google Spread Sheets
from oauth2client.client import SignedJwtAssertionCredentials  # Authention related

from IntraStratagies import open_high_low as olh
from utils import trade_utils, db_utils
from conf import constants, config

# Get the base project Dir
BASEDIR = os.path.dirname(os.getcwd())
# CONFDIR = BASEDIR+os.sep+"conf"
CONFDIR = "conf"
# Credential file
CREDENTIALS_FILE = CONFDIR + os.sep + "creds.json"

# Load Credentials
JSON_KEY = json.load(open(CREDENTIALS_FILE))
SCOPE = ['https://spreadsheets.google.com/feeds']
# Get the Credentials from 'client_email' and 'private_key'
CREDENTIALS = SignedJwtAssertionCredentials(JSON_KEY['client_email']
                                            , JSON_KEY['private_key'].encode()
                                            , SCOPE)
# Authorize Google Client using Credentials
CLIENT = gspread.authorize(CREDENTIALS)

if __name__ == "__main__":
    OLH_SCRIPTS = olh.sheets_get_olh_data(CLIENT)
    # print([str(x) for x in olh_scripts])
    OLH_TRADES = olh.sheets_generate_olh_trade_data(OLH_SCRIPTS)

    FILE_NAME = constants.FILES_LOCATION + os.sep + time.strftime(constants.FILE_TIME_FORMAT) \
                + constants.FILE_PDF_EXTENSION
    trade_utils.generate_pdf_olh_intra(OLH_TRADES, FILE_NAME)
    trade_utils.sendMail(FILE_NAME)

    db_utils.execute_delete_query(dbhost=config.DB_HOST
                                  , dbname=config.DB_NAME
                                  , dbpassword=config.DB_PASSWORD
                                  , dbuser=config.DB_USER
                                  , tablename=config.DB_INTRA_OLH_TRADE_TABLENAME
                                  , params=
                                  {constants.INTRA_OLH_TRADE_TRADE_DATE:
                                       datetime.datetime.today().strftime(constants.DATE_FORMAT)
                                  }
                                 )

    # Load table 'intra_olh_trade' with olh_trade_data
    trade_utils.insert_olh_intra_trade_db(olh_trade_class_list=OLH_TRADES
                                          , dbhost=config.DB_HOST
                                          , dbname=config.DB_NAME
                                          , dbpassword=config.DB_PASSWORD
                                          , dbuser=config.DB_USER
                                          , tablename=config.DB_INTRA_OLH_TRADE_TABLENAME
                                         )
