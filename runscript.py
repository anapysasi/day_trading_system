import pandas as pd
from sklearn.linear_model import LogisticRegression
from feature_engineering import features_df
from create_df import data_to_df


class DIRECTION:

    BUY = 1
    SELL = -1
    HOLD = 0


class Strategy:
    """
    This strategy will use the logistic regression
    The logistic regression will fit the model at the 30th minute
    When the model is built, we will use the function predict to know if we need to send a buy or sell order.
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
        self.Volatility = list()
        self.momentum = list()
        self.rsi = list()
        self.macd = list()
        self.min5 = list()
        self.min10 = list()
        self.min30 = list()
        self.change = list()
        self._return = list()
        self.vol_pct_change = list()
        self.y = list()
        self.model = LogisticRegression(solver='lbfgs', random_state=0, max_iter=1000)

    def prepare_dataframe(self, original):
        self.datetime.append(original['Datetime'])
        self._open.append(original['Open'])
        self.high.append(original['High'])
        self.low.append(original['Low'])
        self.close.append(original['Close'])
        self.volume.append(original['Volume'])
        data_df = data_to_df(self.datetime, self._open, self.high, self.low, self.close, self.volume)
        return data_df

    def getting_features(self, original):
        data_df = self.prepare_dataframe(original)
        price_update = features_df(data_df)
        return price_update

    def fit(self, original):
        price_update = self.getting_features(original)
 
        self.price.append(price_update['Close'])
        self.high_low.append(price_update['High'] - price_update['Low'])
        self.open_close.append(price_update['Open'] - price_update['Close'])
        self.Volatility.append(price_update['Volatility'])
        # self.momentum.append(price_update['Momentum'])
        # self.rsi.append(price_update['RSI'])
        self.macd.append(price_update['MACD'])
        self.min5.append(price_update['5min'])
        self.min10.append(price_update['10min'])
        self.min30.append(price_update['30min'])
        self.change.append(price_update['Change'])
        self._return.append(price_update['Return'])
        self.vol_pct_change.append(price_update['volume change_pct'])

        if len(self.price) > 1:
            if self.price[len(self.price) - 1] > self.price[len(self.price) - 2]:
                self.y.append(1)
            else:
                self.y.append(-1)
        else:
            self.y.append(-1)

        if len(self.price) > 40:
            fit_x = pd.DataFrame({'Open-Close': self.open_close[30:], 'High-Low': self.high_low[30:],
                                  'Volatility': self.Volatility[30:],
                                  # 'Volatility': self.Volatility[30:], 'Momentum': self.momentum[30:], 'RSI': self.rsi[30:],
                                  'MACD': self.macd[30:], '5min': self.min5[30:],
                                  '10min': self.min10[30:], '30min': self.min30[30:], 'Change': self.change[30:],
                                  'Return': self._return[30:], 'VolChangePct': self.vol_pct_change[30:]})
            fit_y = pd.DataFrame({'Predictor': self.y[30:]})
            self.model.fit(fit_x, fit_y.values.ravel())

    def predict(self, original):
        price_update = self.getting_features(original)
        if len(self.price) > 40:
            predict_value = self.model.predict(
                [[price_update['Open'] - price_update['Close'], price_update['High'] - price_update['Low'],
                  price_update['Volatility'],  price_update['MACD'],
                  # price_update['Volatility'], price_update['Momentum'], price_update['RSI'], price_update['MACD'],
                  price_update['5min'], price_update['10min'], price_update['30min'], price_update['Change'],
                  price_update['Return'], price_update['volume change_pct']]])
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


class ForLoopBackTester:

    def __init__(self, start=None):
        self.list_position = []
        self.list_cash = []
        self.list_holdings = []
        self.list_total = []

        self.position = 0
        self.cash = 100000
        self.total = 0
        self.holdings = 0

        self.strategy = start

    def on_market_data_deceived(self, price_update):
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

    def buy_sell_or_hold_something(self, price_update, _action):
        if _action == 'buy':
            cash_needed = 10 * price_update['Close']
            if self.cash - cash_needed >= 0:
                print(str(price_update['Datetime']) +
                      " send buy order for 10 shares price=%.2f" % (price_update['Close']))
                self.position += 10
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')

        if _action == 'sell':
            position_allowed = 10
            if self.position - position_allowed >= -position_allowed:
                print(str(price_update['Datetime']) +
                      " send sell order for 10 shares price=%.2f" % (price_update['Close']))
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['Close']
            else:
                print('sell impossible because not enough position')

        self.holdings = self.position * price_update['Close']
        self.total = (self.holdings + self.cash)
        print('%s total=%d, holding=%d, cash=%d' %
              (str(price_update['Datetime']), self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings + self.cash)


if __name__ == '__main__':
    naive_backtester = ForLoopBackTester(Strategy())
    reader = pd.read_csv('OneDayData.csv')
    symbols = list('FB')
    num_to_select = 1

    N = len(reader[reader['Symbol'] == 'FB'])
    for j in range(N):
        for i in range(num_to_select):
            send = reader[reader['Symbol'] == 'FB']
            send = send.iloc[j]
            send = send.to_dict()


            _action = naive_backtester.on_market_data_deceived(send)
            naive_backtester.buy_sell_or_hold_something(send, _action)

            
