import numpy as np
import pandas as pd
from scipy import stats
pd.set_option('display.max_columns', None)


def momentum(data, n_min):
    mmt = (data - data.shift(n_min)).fillna(0)
    m = np.where(mmt > 0, 1, 0)
    return m[-1]


# Relative Strength Index
def rsi(stock):
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


# Moving Average Convergence/Divergence
def macd(stock):
    exp1 = stock.Close.ewm(span=12, adjust=False).mean()
    exp2 = stock.Close.ewm(span=26, adjust=False).mean()
    macd_val = exp1 - exp2
    macd_signal = macd_val.ewm(span=9, adjust=False).mean()
    return macd_val, macd_signal


def bollinger_bands(stock, window=20):
    rolling_mean = stock.Close.rolling(window).mean()
    rolling_std = stock.Close.rolling(window).std()
    upper_band = rolling_mean + (rolling_std*2)
    lower_band = rolling_mean - (rolling_std*2)
    return upper_band, lower_band


def features_df(stocks):

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
