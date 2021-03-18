"""
Gets the original data with all the features and fits a model with it.
It also predicts the following value using said model and decides whether it holds, buys, or sells.
"""

from market_actions_strategy1 import DIRECTION
from create_df import data_to_df
from feature_engineering import features_df


class Strategy:
    """
    Predicts if it needs to send a buy or sell order with the values of the
    oscillator and (high/low) bands ensemble.
    """

    def __init__(self):
        self.buy = True
        self.sell = False
        self.datetime = list()
        self._open = list()
        self.high = list()
        self.low = list()
        self.close = list()
        self.volume = list()
        self.price = list()
        self.awesome_oscillator = list()
        self.hband_indicator = list()
        self.lband_indicator = list()

    def prepare_dataframe(self, original):
        """
        returns a dataframe with the data that has been received at the present and all the past values.
        :param original: dictionary with: 'Datetime', 'Open', 'High', 'Low', 'Close',
                             'Volume', 'Dividends', 'Stock Splits' and 'Symbol' as columns
        :return: dataframe with all the values obtained until the moment the function is run (present and past values).
        """
        self.datetime.append(original['Datetime'])
        self._open.append(original['Open'])
        self.high.append(original['High'])
        self.low.append(original['Low'])
        self.close.append(original['Close'])
        self.volume.append(original['Volume'])
        data_df = data_to_df(self.datetime, self._open, self.high, self.low, self.close, self.volume)
        return data_df

    def getting_features(self, original):
        """
        :param original: dictionary with: 'Datetime', 'Open', 'High', 'Low', 'Close',
                         'Volume', 'Dividends', 'Stock Splits' and 'Symbol' as columns
        :return: dataframe with the data that has been received at the present and all the past values
        adding the columns calculated in features_df (awesome_oscillator_val, hband_indicator, lband_indicator).
        """
        data_df = self.prepare_dataframe(original)
        price_update = features_df(data_df, awesome_oscillator_val=True, hband_indicator=True, lband_indicator=True)
        return price_update

    def predict(self, original):
        """
        Predicts what the next value is going to be using the present one.
        Depending on this output sends a hold, buy or sell order.
        :param original: dictionary with: 'Datetime', 'Open', 'High', 'Low', 'Close',
                         'Volume', 'Dividends', 'Stock Splits' and 'Symbol' as columns
        :return: element from the DIRECTION class: BUY, SELL or HOLD.
        """
        price_update = self.getting_features(original)
        self.price.append(price_update['Close'])
        self.awesome_oscillator.append(price_update['awesome_oscillator'])
        self.hband_indicator.append(price_update['hband_indicator'])
        self.lband_indicator.append(price_update['lband_indicator'])
        if len(self.price) > 40:
            predict_value = 0
            if self.awesome_oscillator[-1] < 0 or self.lband_indicator == 1:
                predict_value = 1
            elif self.awesome_oscillator[-1] > 0 or self.hband_indicator == 1:
                predict_value = -1

            if predict_value == 1 and self.buy:
                self.sell = True
                self.buy = False
                return DIRECTION.BUY
            elif predict_value == -1 and self.sell:
                self.sell = False
                self.buy = True
                return DIRECTION.SELL
            else:
                return DIRECTION.HOLD
