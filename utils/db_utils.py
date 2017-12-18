'''
    This will contains utilities related to Database.

'''

import pymysql
from sqlalchemy import create_engine, MetaData, TEXT, Integer, Float, Table, Column, \
    ForeignKey, String, BIGINT, DATE, DATETIME, text
from conf import constants

def load_db_table(ticker, df, dbname, dbhost, dbuser, dbpassword, table):
    '''
    load data frame into database.
    :param ticker:
    :param df:
    :param dbname:
    :param dbhost:
    :param dbuser:
    :param dbpassword:
    :param table
    :return:
    '''
    #df = df.set_index('TradeTime','ticker')
    conn_string = "mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}".format(
        dbuser = dbuser
        , dbpassword = dbpassword
        , dbhost = dbhost
        , dbname = dbname
    )
    engine = create_engine(conn_string)
    meta = MetaData(bind=engine)
    meta.create_all(engine)
    print("loading Symbol %s - table %s" % (ticker, table))
    params = {'name':table
              , 'con' : engine
              , 'chunksize' : 1000
              , 'if_exists' : 'append'
              , 'index' : False
              }
    try:
        df.to_sql(**params)
    except Exception as ex:
        print (str(ex))
        return False
    return True


def load_eod_db(ticker, df, dbname, dbhost, dbuser, dbpassword, table):
    '''
    load data frame into database.
    :param ticker:
    :param df:
    :param dbname:
    :param dbhost:
    :param dbuser:
    :param dbpassword:
    :param eod table
    :return:
    '''
    df['TradeDate'] = df['TradeTime'].dt.date
    #df = df.set_index('TradeTime','ticker')
    conn_string = "mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}".format(
        dbuser = dbuser
        , dbpassword = dbpassword
        , dbhost = dbhost
        , dbname = dbname
    )
    engine = create_engine(conn_string)
    meta = MetaData(bind=engine)
    meta.create_all(engine)
    print("loading Symbol %s - table %s" % (ticker, table))
    params = {'name':table
              , 'con' : engine
              , 'chunksize' : 1000
              , 'if_exists' : 'append'
              , 'index' : False
              }
    try:
        df.to_sql(**params)
    except Exception as ex:
        print (str(ex))
        return False
    return True

def execute_simple_db_query(query, dbname, dbhost, dbuser, dbpassword):
    '''
    This will execute query
    :param query:
    :param dbname:
    :param dbhost:
    :param dbuser:
    :param dbpassword:
    :return: dictionary with 2 items.
             1. Query status (SUCCESS(1)/FAILURE(0))
             2. Python list of result
    '''
    result_dict = {}
    conn_string = "mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}".format(
        dbuser=dbuser
        , dbpassword=dbpassword
        , dbhost=dbhost
        , dbname=dbname
    )
    engine = create_engine(conn_string)
    with engine.connect() as con:
        try:
            rs = con.execute(query)
            result = []
            result_dict['status']=constants.SUCCESS
            for row in rs:
                result.append(list(row))
            print (type(result[0]))
            result_dict['result'] = result

        except Exception as ex:
            print(str(ex))
            result_dict['status']=constants.FAIL
            result_dict['result'] = []
    return result_dict


def execute_insert_query(tablename, dbname, dbhost, dbuser, dbpassword,params):
    '''
    This will execute query
    :param tablename:
    :param dbname:
    :param dbhost:
    :param dbuser:
    :param dbpassword:
    :param params : dictionary
    :return: SUCCESS/FAIL
    '''

    conn_string = "mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}".format(
        dbuser=dbuser
        , dbpassword=dbpassword
        , dbhost=dbhost
        , dbname=dbname
    )
    engine = create_engine(conn_string)
    column_value_list = [key+":"+key for key in params.keys()]
    insert_columns_text = ','.join(column_value_list)
    insert_text = 'insert into {} values({})'.format(tablename,insert_columns_text)
    print(insert_text)

    text_insert  = text(insert_text)

    with engine.connect() as conn:
        conn.execute(text_insert,**params)
    #print (insert_text)

    #ins = tablename.insert().values(**params)
    #print (str(ins))
    return constants.SUCCESS


