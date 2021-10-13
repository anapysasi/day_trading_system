"""
This file creates a csv file with the data of an specific day within the last seven days.
The data is the information from the 500 stocks from the S&P 500.
You have the information of the stock at every minute that the market is open.
You can use this csv file to run the model.
"""

import pandas as pd
import yfinance as yf
from openpyxl import load_workbook


def create_df(day, save=False, datetime_index=False, list_stocks=None):
    """
    creates a dataframe with the data of the 500 stocks in the S&P 500 by minute for the specified day.
    :param day: The format must be 'YYYY-MM-DD'. You can only choose one day within the last 7 days.
    :param save: Determines if you want to save the data, in that case set True. Default false
    :param datetime_index: if true returns a dataframe with the DateTime column as the index. Default False.
    :param list_stocks: list of stocks to create the dataframe. Default, no list.
    :return data of that day for the stocks.
    """

    if list_stocks is None:
        data = load_workbook('SPY500.xlsx')
        data = data['Sheet1']
        data = data.values
        columns = next(data)[0:]

        df = pd.DataFrame(data, columns=columns)
        symbols = list(df['Symbol'])
    else:
        symbols = list_stocks

    # yfinance changed the API, so there are some stock that dont have information. We need to delete some symbols
    deleted_stocks = ['ALXN', 'MXIM', 'VAR', 'LB', 'COG', 'FLIR']
    for element in deleted_stocks:
        if element in symbols:
            print('Deleted', element, '. Symbol may be delisted from yfinance.')
            symbols.remove(element)

    i = 0
    data0 = yf.Ticker(symbols[i])

    df0 = data0.history(day, interval='1m')
    df0['Symbol'] = [symbols[i]]*df0.shape[0]

    for i in range(1, len(symbols)):
        data = yf.Ticker(symbols[i])
        df = data.history(day, interval='1m')
        df['Symbol'] = [symbols[i]]*df.shape[0]
        df0 = df0.append(df)

    if save is True:
        df0.to_csv('OneDayData%s.csv' % day)

    if datetime_index is True:
        return pd.DataFrame(df0)

    if datetime_index is False:
        df0 = pd.DataFrame(df0)
        df0 = df0.reset_index()
        return df0
