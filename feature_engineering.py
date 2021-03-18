"""
Gets a dataframe and calculates the following features: momentum, relative strength index (RSI),
moving average convergence/divergence, volatility, 5-10 and 30 mins moving average, volume change,
percentage volume change, upper and lower bands and z-score.
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.momentum import PercentagePriceOscillator
from ta.trend import macd
from ta.momentum import awesome_oscillator
from ta.others import daily_return
from ta.volatility import BollingerBands
pd.set_option('display.max_columns', None)


def features_df(stocks):
    """
    Calculates the momentum, RSI, moving average convergence/divergence, volatility,
    5-10 and 30 mins moving average, volume change, pct volume change, upper, lower bands and z-score
    :param stocks: dataframe of stocks
    :return: a dataframe with the different features of said stock
    """
    stocks['rsi_vals'] = RSIIndicator(close=stocks.Close, window=10).rsi()
    stocks['macd_vals'] = macd(stocks.Close, window_slow=26, window_fast=12)
    stocks['Ppo'] = np.array(PercentagePriceOscillator(stocks.Close, window_slow=26, window_fast=12).ppo())
    stocks['awesome_oscillator'] = awesome_oscillator(stocks.High, stocks.Low, window1=5, window2=29)
    stocks['daily_log_return'] = daily_return(close=stocks.Close)
    stocks['Return'] = round(stocks['Close'] / stocks['Open'] - 1, 3)
    stocks['Change'] = (stocks.Close - stocks.Close.shift(1)).fillna(0)
    stocks['Volatility'] = stocks.Close.ewm(21).std()
    stocks['min5'] = stocks.Close.rolling(5).mean()
    stocks['min10'] = stocks.Close.rolling(10).mean()
    stocks['min30'] = stocks.Close.rolling(30).mean()
    stocks['hband_indicator'] = BollingerBands(close=stocks.Close).bollinger_hband_indicator()
    stocks['lband_indicator'] = BollingerBands(close=stocks.Close).bollinger_lband_indicator()
    stocks['Corr'] = stocks.Close.rolling(window=10).corr(stocks['min10'])

    return stocks.iloc[-1, :]
