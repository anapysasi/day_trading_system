import pandas as pd
import trading_strategy as ts
import market_actions as ma


class DIRECTION:

    BUY = 1
    SELL = -1
    HOLD = 0


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

    def on_market_data_received(self, price_update):
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
#     strategy = ts.Strategy()
#     market = ma.MarketActions(strategy)

    strategy_dic = {}
    market_dic = {}
    dic = {}
    reader = pd.read_csv('OneDayData.csv')
    symbols = list('WRK')
    num_to_select = 1

    strategy_dic['strategy' + str(symbols[0])] = ts.Strategy()
    market_dic['market' + str(symbols[0])] = ma.MarketActions(strategy_dic['strategy' + str(symbols[0])])

    N = len(reader[reader['Symbol'] == 'WRK'])
    for j in range(N):
        for i in range(num_to_select):
            send = reader[reader['Symbol'] == 'WRK']
            send = send.iloc[j]
            send = send.to_dict()

            _action = naive_backtester.on_market_data_received(send)
            naive_backtester.buy_sell_or_hold_something(send, _action)
            # _action = market.on_market_data_received(send)
            # market.buy_sell_or_hold_something(send, _action)

            dic['_action' + str(symbols[0])] = market_dic['market' + str(symbols[0])].on_market_data_received(send)
            market_dic['market' + str(symbols[0])].buy_sell_or_hold_something(send, dic['_action' + str(symbols[0])])
