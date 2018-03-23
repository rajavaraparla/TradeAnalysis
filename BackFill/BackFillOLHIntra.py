"""
    BackFill OpenHighLow Strategy
"""
from datetime import date, timedelta
from utils import trade_utils, db_utils
from conf import constants, config


def backfill_intra_olh_trades(from_date, to_date=date.today()):
    '''
    This will fill the table intra_olh_trade
    :param from_date:
    :param to_date:
    :return:
    '''
    delta = to_date - from_date
    for p_delta in range(delta.days):
        curr_date = from_date + timedelta(p_delta)
        print(
            "Filling TradeData for Date - " +
            curr_date.strftime(
                constants.DATE_FORMAT))
        olh_class_list = db_utils.get_olh_class_list(
            p_date=curr_date,
            dbhost=config.DB_HOST,
            dbuser=config.DB_USER,
            dbpassword=config.DB_PASSWORD,
            dbname=config.DB_NAME,
            timeframe=constants.TIME_15MIN,
            p_time=constants.TIME_930)

        for olh_class in olh_class_list:
            db_utils.execute_delete_query(
                dbhost=config.DB_HOST,
                dbname=config.DB_NAME,
                dbpassword=config.DB_PASSWORD,
                dbuser=config.DB_USER,
                tablename=config.DB_INTRA_OLH_TRADE_TABLENAME,
                params={
                    constants.INTRA_OLH_TRADE_TRADE_DATE: curr_date.strftime(
                        constants.DATE_FORMAT)})
            # Load table 'intra_olh_trade' with olh_trade_data
            trade_utils.insert_olh_intra_trade_db(
                olh_trade_class_list=olh_class_list,
                dbhost=config.DB_HOST,
                dbname=config.DB_NAME,
                dbpassword=config.DB_PASSWORD,
                dbuser=config.DB_USER,
                tablename=config.DB_INTRA_OLH_TRADE_TABLENAME)
        #print (from_date+timedelta(p_delta))
    # Get data from
    # db_utils.get_intra_candle(date=)


if __name__ == '__main__':
    backfill_intra_olh_trades(
        date.today() - timedelta(1),
        to_date=date.today())
