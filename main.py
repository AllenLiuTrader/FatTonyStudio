from alpha_vantage.timeseries import TimeSeries
import sys
import requests
from pprint import pprint


def update_symbols():
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
                symbol_pool.append(symbol)

    symbol_pool.sort()


def fetch_data():
    app = TimeSeries()
    data, meta_data = app.get_intraday('AAL')
    pprint(meta_data)


if __name__ == '__main__':
    opt = sys.argv[1]

    if opt == 'update_symbols':
        update_symbols()
    elif opt == 'fetch_data':
        fetch_data()
