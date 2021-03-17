"""
Gets a set of lists and creates a dataframe with them.
"""
import pandas as pd
import numpy as np


def data_to_df(datetime, _open, high, low, close, volume):
    """
    Gets a set of lists and creates a dataframe with them.
    :param datetime: list with the date and time of the data
    :param _open: list with the open value of the stock
    :param high: list with the high value of the stock
    :param low: list with the low value of the stock
    :param close: list with the close price of the stock
    :param volume: list with the volume of the stock
    :return: dataframe with all the input lists as columns
    """
    datetime_df = pd.DataFrame(np.array(datetime))
    open_df = pd.DataFrame(np.array(_open))
    high_df = pd.DataFrame(np.array(high))
    low_df = pd.DataFrame(np.array(low))
    close_df = pd.DataFrame(np.array(close))
    volume_df = pd.DataFrame(np.array(volume))

    concat_df = pd.concat([datetime_df, open_df, high_df, low_df, close_df, volume_df], axis=1)
    concat_df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']

    return concat_df
