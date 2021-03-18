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


def features_df(stocks, rsi_vals=False, macd_vals=False, ppo=False,
                awesome_oscillator_val=False, daily_log_return=False,
                _return=False, change=False, volatility=False, min5=False,
                min10=False, min30=False, hband_indicator=False,
                lband_indicator=False, corr=False):
    """
    Calculates the momentum, RSI, moving average convergence/divergence (MACD), Percentage Price Oscillator,
    awesome oscillator indicator, daily log return column, return, change, volatility, 5-10 and 30 mins moving average,
    high band indicator, lower band indicator, correlation of the given stock dataframe.
    :param stocks: dataframe of stocks
    :param rsi_vals: Default value False. If you want the RSI column, set True
    :param macd_vals: Default value False. If you want the MACD column, set True
    :param ppo: Default value False. If you want the Percentage Price Oscillator column, set True
    :param awesome_oscillator_val: Default value False. If you want the awesome oscillator indicator column, set True
    :param daily_log_return: Default value False. If you want the daily log return column, set True
    :param _return: Default value False. If you want the return column, set True
    :param change: Default value False. If you want the change column, set True
    :param volatility: Default value False. If you want the volatility column, set True
    :param min5: Default value False. If you want the min5 column, set True
    :param min10: Default value False. If you want the min10 column, set True
    :param min30: Default value False. If you want the min30 column, set True
    :param hband_indicator: Default value False. If you want the high band indicator column, set True
    :param lband_indicator: Default value False. If you want the lower band indicator column, set True
    :param corr: Default value False. If you want the correlation column, set True
    :return: a dataframe with the different features of said stock Default value False.
                If you want the RSI column, set True
    """

    if rsi_vals is True:
        stocks['rsi_vals'] = RSIIndicator(close=stocks.Close, window=10).rsi()
    if macd_vals is True:
        stocks['macd_vals'] = macd(stocks.Close, window_slow=26, window_fast=12)
    if ppo is True:
        stocks['Ppo'] = np.array(PercentagePriceOscillator(stocks.Close, window_slow=26, window_fast=12).ppo())
    if awesome_oscillator_val is True:
        stocks['awesome_oscillator'] = awesome_oscillator(stocks.High, stocks.Low, window1=5, window2=29)
    if daily_log_return is True:
        stocks['daily_log_return'] = daily_return(close=stocks.Close)
    if _return is True:
        stocks['Return'] = round(stocks['Close'] / stocks['Open'] - 1, 3)
    if change is True:
        stocks['Change'] = (stocks.Close - stocks.Close.shift(1)).fillna(0)
    if volatility is True:
        stocks['Volatility'] = stocks.Close.ewm(21).std()
    if min5 is True:
        stocks['min5'] = stocks.Close.rolling(5).mean()
    if min10 is True:
        stocks['min10'] = stocks.Close.rolling(10).mean()
    if min30 is True:
        stocks['min30'] = stocks.Close.rolling(30).mean()
    if hband_indicator is True:
        stocks['hband_indicator'] = BollingerBands(close=stocks.Close).bollinger_hband_indicator()
    if lband_indicator is True:
        stocks['lband_indicator'] = BollingerBands(close=stocks.Close).bollinger_lband_indicator()
    if corr is True:
        stocks['Corr'] = stocks.Close.rolling(window=10).corr(stocks['min10'])

    return stocks.iloc[-1, :]
