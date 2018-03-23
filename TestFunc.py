from utils import common_utils
import datetime
import pandas as pd

#ohlc_ds = common_utils.get_eod_ohlc_data(from_date='2018-02-20',to_date='2018-02-27',ticker='SUNPHARMA')
#intra_ohlc_ds = common_utils.get_intra_ohlc_first_15min_candle(from_date=datetime.date(2018,3,15),start_time=datetime.time(9,30,0),end_time=datetime.time(10,30,0),ticker='SUNPHARMA')
intra_ohlc_ds = common_utils.get_intra_ohlc_first_15min_candle(from_date=datetime.date(2018,3,15),ticker='DRREDDY')

df = pd.DataFrame(intra_ohlc_ds['result'],columns=['Ticker','Date','Time','Open','High','Low','Close','Vwap','Volume'])
print(df)
exit(1)
print (intra_ohlc_ds['result'])

for intra_ohlc_candle in intra_ohlc_ds['result']:
    print(intra_ohlc_candle)