"""
Gets the original data with all the features and fits a model with it.
It also predicts the following value using said model and decides whether it holds, buys, or sells.
"""

from market_actions_strategy1 import DIRECTION
from create_df import data_to_df
from sklearn.linear_model import LogisticRegression
from feature_engineering import features_df
import pandas as pd


class Strategy:
    """
    Fits the data to a logistic regression.
    The logistic regression will fit the model at the 30th minute.
    It will actualize the model every time it gets a new line of data.
    It also predicts if we need to send a buy or sell order.
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
        self.high_low = list()
        self.open_close = list()
        self.price = list()
        self.awesome_oscillator = list()
        self.daily_log_return = list()
        self.Change = list()
        self.Volatility = list()
        self.min10 = list()
        self.hband_indicator = list()
        self.lband_indicator = list()
        self.y = list()
        self.model = LogisticRegression(solver='lbfgs', random_state=0, max_iter=4000)


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
        adding the columns calculated in features_df (awesome_oscillator_val, daily_log_return, change,
                                   volatility, min10=True, hband_indicator, lband_indicator).
        """
        data_df = self.prepare_dataframe(original)
        price_update = features_df(data_df, awesome_oscillator_val=True, daily_log_return=True, change=True,
                                   volatility=True, min10=True, hband_indicator=True, lband_indicator=True)
        return price_update

    def fit(self, original):
        """
        :param original: dictionary with: 'Datetime', 'Open', 'High', 'Low', 'Close',
                         'Volume', 'Dividends', 'Stock Splits' and 'Symbol' as columns
        :return: model fit using all the original data and all the features.
        """
        price_update = self.getting_features(original)
        # Appending to appropriate lists
        self.price.append(price_update['Close'])
        self.high_low.append(price_update['High'] - price_update['Low'])
        self.open_close.append(price_update['Open'] - price_update['Close'])
        self.awesome_oscillator.append(price_update['awesome_oscillator'])
        self.daily_log_return.append(price_update['daily_log_return'])
        self.Change.append(price_update['Change'])
        self.Volatility.append(price_update['Volatility'])
        self.min10.append(price_update['min10'])
        self.hband_indicator.append(price_update['hband_indicator'])
        self.lband_indicator.append(price_update['lband_indicator'])

        if len(self.price) > 1:
            if self.price[len(self.price) - 1] > self.price[len(self.price) - 2]:
                self.y.append(1)
            else:
                self.y.append(-1)
        else:
            self.y.append(-1)

        if len(self.price) > 40:
            fit_x = pd.DataFrame({'Open-Close': self.open_close[30:], 'High-Low': self.high_low[30:],
                                  'Change': self.Change[30:], 'Volatility': self.Volatility[30:],
                                  'min10': self.min10[30:], 'hband_indicator': self.hband_indicator[30:],
                                  'lband_indicator': self.lband_indicator[30:], 'awesome_oscillator': self.awesome_oscillator[30:],
                                  'daily_log_return': self.daily_log_return[30:]})
            fit_y = pd.DataFrame({'Predictor': self.y[30:]})
            self.model.fit(fit_x, fit_y.values.ravel())

    def predict(self, original):
        """
        Predicts what the next value is going to be using the present one.
        Depending on this output sends a hold, buy or sell order.
        :param original: dictionary with: 'Datetime', 'Open', 'High', 'Low', 'Close',
                         'Volume', 'Dividends', 'Stock Splits' and 'Symbol' as columns
        :return: element from the DIRECTION class: BUY, SELL or HOLD.
        """
        price_update = self.getting_features(original)
        if len(self.price) > 40:
            predict_value = self.model.predict(
                [[price_update['Open'] - price_update['Close'], price_update['High'] - price_update['Low'],
                  price_update['Change'], price_update['Volatility'], price_update['min10'],
                  price_update['hband_indicator'], price_update['lband_indicator'],
                  price_update['awesome_oscillator'], price_update['daily_log_return']]])
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
