
from utils import db_utils
from conf import config
from datetime import datetime

if __name__ == '__main__':
    query = "select * from hist_data where TradeDate = '2017-12-06'"
    print(db_utils.execute_simple_db_query(query, config.DB_NAME, config.DB_HOST, config.DB_USER, config.DB_PASSWORD))

    pass