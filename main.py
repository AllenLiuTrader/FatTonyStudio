from alpha_vantage.timeseries import TimeSeries
import sys
import os
import pymongo
import requests
from pprint import pprint


def connect_mongo():
    mongo_conn = os.environ['MONGO_CONN']
    conn = pymongo.MongoClient(mongo_conn)
    db = conn['us_stock']
    return db


def opt_update_symbols():
    def assemble_url(market):
        return f'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange={market}&render=download'

    symbol_pool = []

    for market in ['nasdaq', 'nyse', 'amex']:
        url = assemble_url(market)
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'

        headers = {
            'user-agent': ua
        }

        r = requests.get(url, headers=headers)
        companies = r.text.split('\r\n')[1:]

        for company in companies:
            symbol = company.split(',')[0].strip('"')

            if symbol:
                symbol_pool.append({'name': symbol})

    db = connect_mongo()
    collection = db['symbol']
    collection.insert_many(symbol_pool)
    pprint(len(symbol_pool))


def opt_fetch_data():
    app = TimeSeries()
    data, meta_data = app.get_intraday('AAL')
    pprint(meta_data)


if __name__ == '__main__':
    opt = sys.argv[1]

    if opt == 'update_symbols':
        opt_update_symbols()
    elif opt == 'fetch_data':
        opt_fetch_data()
