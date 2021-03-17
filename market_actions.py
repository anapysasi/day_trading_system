class DIRECTION:

    BUY = 1
    SELL = -1
    HOLD = 0


class MarketActions:

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
        self.news = None

    def received_market_data(self, price_update):
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

    def action_buy_sell_hold(self, price_update, _action):
        if _action == 'buy':
            cash_needed = 10 * price_update['Close']
            if self.cash - cash_needed >= 0:
                self.news = str(str(price_update['Datetime']) + " send buy order for 10 shares price=%.2f" %
                                (price_update['Close']))
                self.position += 10
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')

        if _action == 'sell':
            position_allowed = 10
            if self.position - position_allowed >= -position_allowed:
                self.news = str(str(price_update['Datetime']) + " send sell order for 10 shares price=%.2f" %
                                (price_update['Close']))
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['Close']
            else:
                print('sell impossible because not enough position')

        if _action == 'hold':
            self.news = None

        self.holdings = self.position * price_update['Close']
        self.total = (self.holdings + self.cash)

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings + self.cash)

        return self.total, self.holdings, self.cash, self.news
