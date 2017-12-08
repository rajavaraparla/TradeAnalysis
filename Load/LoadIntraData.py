'''
Get Intraday data

'''

from conf import config
from conf import constants
from utils import trade_utils, db_utils




if __name__ == "__main__":
    #print(trade_utils.get_google_finance_intraday("CIPLA",period=300,days=1))
    # Get last 90 days data.
    SYMBOLS = constants.ALL_SYMBOLS
    NUM_DAYS = 1

    for index,ticker in enumerate(SYMBOLS):
        DF_5MIN = trade_utils.get_intra_5min_data(ticker=ticker, days=NUM_DAYS)
        RESULT_5MIN = db_utils.load_db_table(
            ticker
            , DF_5MIN
            , config.DB_NAME
            , config.DB_HOST
            , config.DB_USER
            , config.DB_PASSWORD
            , config.DB_INTRA_5MIN_TABLE
        )

        DF_15MIN = trade_utils.get_intra_15min_data(ticker=ticker, days=NUM_DAYS)
        RESULT_5MIN = db_utils.load_db_table(
            ticker
            , DF_15MIN
            , config.DB_NAME
            , config.DB_HOST
            , config.DB_USER
            , config.DB_PASSWORD
            , config.DB_INTRA_15MIN_TABLE
        )

        DF_30MIN = trade_utils.get_intra_30min_data(ticker=ticker, days=NUM_DAYS)
        RESULT_5MIN = db_utils.load_db_table(
            ticker
            , DF_30MIN
            , config.DB_NAME
            , config.DB_HOST
            , config.DB_USER
            , config.DB_PASSWORD
            , config.DB_INTRA_30MIN_TABLE
        )

        DF_HOUR = trade_utils.get_intra_hour_data(ticker=ticker, days=NUM_DAYS)
        RESULT_5MIN = db_utils.load_db_table(
            ticker
            , DF_HOUR
            , config.DB_NAME
            , config.DB_HOST
            , config.DB_USER
            , config.DB_PASSWORD
            , config.DB_INTRA_HOUR_TABLE
        )


    #print(get_intra_30min_data("BAJAJ-AUTO", days=1))
    #print(get_intra_hour_data("BAJAJ-AUTO", days=1))



