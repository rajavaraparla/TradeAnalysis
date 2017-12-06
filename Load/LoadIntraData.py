'''
Get Intraday data

'''

from utils import trade_utils

def get_intra_15min_data(ticker,days=1):
    return trade_utils.get_google_finance_intraday(ticker, period=300, days=days)

def get_intra_30min_data(ticker, days=1):
    return trade_utils.get_google_finance_intraday(ticker, period=1800, days=days)

def get_intra_hour_data(ticker, days=1):
    return trade_utils.get_google_finance_intraday(ticker, period=3600, days=days)



if __name__ == "__main__":
    #print(trade_utils.get_google_finance_intraday("CIPLA",period=300,days=1))
    print(get_intra_15min_data("BAJAJ-AUTO",days=300))
    #print(get_intra_30min_data("BAJAJ-AUTO", days=1))
    print(get_intra_hour_data("BAJAJ-AUTO", days=1))



