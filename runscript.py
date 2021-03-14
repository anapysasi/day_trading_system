import math
import os
import random
import re
import sys
import pandas as pd
from abc import ABC
from collections import deque
from sklearn.linear_model import LogisticRegression
from feature_engineering import features_df


class DIRECTION:
    BUY = 1
    SELL = -1
    HOLD = 0


class strategy3:
    '''
    This stragety will use the logistic regresion
    The logistic regresion will fit the model at the 30th minute
    When the model is built, we will use the function predict to know if we need to send a buy or sell order.
    '''

# 5min, 10min, 30min, volumn change,
    def __init__(self):
        self.buy = True
        self.sell = False
        self.HighLow = deque()
        self.OpenClose = deque()
        self.Price = deque()
        self.Volatility = deque()
        self.Momentum = deque()
        self.RSI = deque()
        self.MACD = deque()
        self.Min5 = deque()
        self.Min10 = deque()
        self.Min30 = deque()
        self.Change = deque()
        self.Return = deque()
        self.VolChangePct = deque()
        self.y = deque()
        self.model = LogisticRegression(solver = 'lbfgs', random_state = 0)




    def prepare_dataframe(self, original):
        aapl = pd.read_csv('/Users/maggiewu/Downloads/OneDayDataAPPL.csv')
        return aapl
        # return dataframe
    def getting_features(self, original):
        price_update = features_df(prepare_dataframe(original))
        return price_update

    def fit(self, price_update):
        # self.Price.append(price_update['price'])
        self.Price.append(price_update['Close'])
        self.HighLow.append(price_update['High'] - price_update['Low'])
        self.OpenClose.append(price_update['Open'] - price_update['Close'])
        self.Volatility.append(price_update['Volatility'])
        self.Momentum.append(price_update['Momentum'])
        self.RSI.append(price_update['RSI'])
        self.MACD.append(price_update['MACD'])
        self.Min5.append(price_update['5min'])
        self.Min10.append(price_update['10min'])
        self.Min30.append(price_update['30min'])
        self.Change.append(price_update['Change'])
        self.Return.append(price_update['Return'])
        self.VolChangePct.append(price_update['volume change_pct'])

        #y = np.where(self.df_list['price'].shift(1).fillna(0)<self.df_list['price'], 1, -1)
        if len(self.Price) > 1:
            if self.Price[len(self.Price) - 1] > self.Price[len(self.Price) - 2]:
                self.y.append(1)
            else:
                self.y.append(-1)
        else:
            self.y.append(-1)

        if len(self.Price) == 30:
            fitX = pd.DataFrame({'Open-Close': self.OpenClose, 'High-Low': self.HighLow, 'Volatility': self.Volatility,
                                 'Momentum': self.Momentum, 'RSI': self.RSI, 'MACD': self.MACD, '5min': self.Min5,
                                 '10min': self.Min10, '30min': self.Min30, 'Change': self.Change, 'Return': self.Return,
                                 'VolChangePct': self.VolChangePct})
            fitY = pd.DataFrame({'Predictor': self.y})
            self.model.fit(fitX, fitY.values.ravel())

    def predict(self, price_update):
        if len(self.Price) > 30:
            predict_value = self.model.predict(
                [[price_update['open'] - price_update['close'], price_update['high'] - price_update['low'], price_update['Volatility'],
                  price_update['Momentum'], price_update['RSI'], price_update['MACD'], price_update['5min'], price_update['10min'],
                  price_update['30min'], price_update['Change'], price_update['Return'], price_update['volume change_pct']]])
            if predict_value == 1 and self.buy:
                self.sell = True
                self.buy = False
                return DIRECTION.BUY
            elif predict_value == -1 and self.sell:
                self.sell = False
                self.buy = True
                return DIRECTION.SELL

class ForLoopBackTester:
    def __init__(self, strat=None):
        self.list_position = []
        self.list_cash = []
        self.list_holdings = []
        self.list_total = []

        self.long_signal = False
        self.position = 0
        self.cash = 100000
        self.total = 0
        self.holdings = 0

        self.market_data_count = 0
        self.prev_price = None
        self.statistical_model = None
        self.historical_data = pd.DataFrame(columns=['Trade', 'Price', 'OpenClose', 'HighLow'])
        self.strategy = strat

    def onMarketDataReceived(self, price_update):
        if self.strategy:
            self.strategy.fit(price_update)
            predicted_value = self.strategy.predict(price_update)
        else:
            predicted_value = DIRECTION.HOLD

        if predicted_value == DIRECTION.BUY:
            return 'buy'
        if predicted_value == DIRECTION.SELL:
            return 'sell'
        return 'hold'

    def buy_sell_or_hold_something(self, price_update, action):
        if action == 'buy':
            cash_needed = 10 * price_update['Price']
            if self.cash - cash_needed >= 0:
                print(str(price_update['date']) +
                      " send buy order for 10 shares price=%.2f" % (price_update['Price']))
                self.position += 10
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')

        if action == 'sell':
            position_allowed = 10
            if self.position - position_allowed >= -position_allowed:
                print(str(price_update['date']) +
                      " send sell order for 10 shares price=%.2f" % (price_update['Price']))
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['Price']
            else:
                print('sell impossible because not enough position')

        self.holdings = self.position * price_update['Price']
        self.total = (self.holdings + self.cash)
        # print('%s total=%d, holding=%d, cash=%d' %
        #       (str(price_update['date']),self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings + self.cash)

naive_backtester = None
nb_of_rows = 0



def test5():
    global naive_backtester
    global nb_of_rows
    nb_of_rows = 600
    naive_backtester = ForLoopBackTester(strategy3())


if __name__ == '__main__':

    aapl = pd.read_csv('aapl.csv')
    aapl['Price'] = aapl['Close']
    for i in range(len(aapl)):
        price_information = aapl.iloc[i, :].to_dict()
        naive_backtester = ForLoopBackTester(strategy3())
        action = naive_backtester.onMarketDataReceived(price_information)
        naive_backtester.buy_sell_or_hold_something(price_information, action)
        #print(price_information, )

    # for _ in range(nb_of_rows):
    #     row = input().strip().split(',')
    #
    #     date = row[0]
    #     high = row[1]
    #     low = row[2]
    #     closep = row[4]
    #     openp = row[3]
    #     volume = row[5]
    #     price = row[6]
    #
    #     price_information = {'date': date,
    #                          'price': float(price),
    #                          'high': float(high),
    #                          'low': float(low),
    #                          'close': float(closep),
    #                          'open': float(openp),
    #                          'volume': float(volume)}
    #     action = naive_backtester.onMarketDataReceived(price_information)
    #     naive_backtester.buy_sell_or_hold_something(price_information, action)

    #print("PNL:%.2f" % (naive_backtester.list_total[-1] - 10000))
