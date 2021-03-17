"""
Gets a dataframe and calculates the following features: momentum, relative strength index (RSI),
moving average convergence/divergence, volatility, 5-10 and 30 mins moving average, volume change,
percentage volume change, upper and lower bands and z-score.
"""

import numpy as np
import pandas as pd
from scipy import stats
pd.set_option('display.max_columns', None)


def momentum(data, n_min):
    """
    Calculates the momentum of a stock for n_days
    """
    mmt = (data - data.shift(n_min)).fillna(0)
    m = np.where(mmt > 0, 1, 0)
    return m[-1]


def rsi(stock):
    """
    Calculates the Relative Strength Index (RSI)
    :param stock: dataframe of stocks
    :return: RSI of said stock
    """
    gain = lambda x: x if x > 0 else 0
    loss = lambda x: abs(x) if x < 0 else 0
    rsi_list = [None] * 14
    stock = stock.Change

    # Calculating RSI
    avg_gain = sum([i for i in stock[1:15] if i > 0]) / 14
    avg_loss = sum([abs(i) for i in stock[1:15] if i < 0]) / 14

    if avg_loss == 0:
        rsi_list.append(0)
    else:
        rs = avg_gain / avg_loss
        rsi_val = 100 - (100 / (1 + rs))
        rsi_list.append(rsi_val)

    for i in range(15, len(stock)):
        avg_gain = (avg_gain * 13 + gain(stock[i])) / 14
        avg_loss = (avg_loss * 13 + loss(stock[i])) / 14

        if avg_loss == 0:
            rsi_list.append(0)
        else:
            rs = avg_gain / avg_loss
            rsi_val = 100 - (100 / (1 + rs))
            rsi_list.append(rsi_val)

    return rsi_list[-1]


def macd(stock):
    """
    Calculates the Moving Average Convergence/Divergence
    :param stock: dataframe of stocks
    :return: Moving Average Convergence/Divergence of said stock
    """
    exp1 = stock.Close.ewm(span=12, adjust=False).mean()
    exp2 = stock.Close.ewm(span=26, adjust=False).mean()
    macd_val = exp1 - exp2
    macd_signal = macd_val.ewm(span=9, adjust=False).mean()
    return macd_val, macd_signal


def bollinger_bands(stock, window=20):
    """
    Calculates the Upper and Lower band of a stock
    :param stock: dataframe of stocks
    :param window: The window for the rolling average. The default value is 20.
    :return: Upper and Lower band of said stock
    """
    rolling_mean = stock.Close.rolling(window).mean()
    rolling_std = stock.Close.rolling(window).std()
    upper_band = rolling_mean + (rolling_std*2)
    lower_band = rolling_mean - (rolling_std*2)
    return upper_band, lower_band


def features_df(stocks):
    """
    Calculates the momentum, RSI, moving average convergence/divergence, volatility,
    5-10 and 30 mins moving average, volume change, pct volume change, upper, lower bands and z-score
    :param stocks: dataframe of stocks
    :return: a dataframe with the different features of said stock
    """
    stocks['Return'] = round(stocks['Close'] / stocks['Open'] - 1, 3)
    stocks['Change'] = (stocks.Close - stocks.Close.shift(1)).fillna(0)
    stocks['Volatility'] = stocks.Close.ewm(21).std()
    stocks['5min'] = stocks.Close.rolling(5).mean()
    stocks['10min'] = stocks.Close.rolling(10).mean()
    stocks['30min'] = stocks.Close.rolling(30).mean()
    stocks['volume change'] = (stocks.Volume - stocks.Volume.shift(1)).fillna(0)
    stocks['volume change_pct'] = stocks['volume change']/stocks['Volume']
    stocks['Momentum'] = momentum(stocks.Close, 3)
    stocks['RSI'] = rsi(stocks)
    stocks['MACD'], stocks['MACD_Signal'] = macd(stocks)
    stocks['upper_band'], stocks['lower_band'] = bollinger_bands(stocks)
    stocks['zscore'] = stats.zscore(stocks['Close'])[-1]
    return stocks.iloc[-1, :]
