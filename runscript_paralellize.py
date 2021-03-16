import pandas as pd
import trading_strategy as ts
import market_actions as ma


if __name__ == '__main__':

    strategy_dic = {}
    market_dic = {}
    dic = {}
    total = {}
    holdings = {}
    cash = {}
    news = {}
    reader = pd.read_csv('OneDayData.csv')
    symbols = ['WRK', 'FB', 'ULTA']
    num_to_select = 3
    list_of_random_items = symbols
    counter = 0

    length = []
    for i in range(num_to_select):
        N = len(reader[reader['Symbol'] == list_of_random_items[i]])
        length.append(N)

    N = min(length)

    for j in range(N):
        for i in range(num_to_select):
            send = reader[reader['Symbol'] == list_of_random_items[i]]
            send = send.iloc[j]
            send = send.to_dict()

            counter += 1
            if counter < (num_to_select + 1):
                strategy_dic['strategy' + str(send["Symbol"])] = ts.Strategy()
                market_dic['market' + str(send["Symbol"])] = ma.MarketActions(
                    strategy_dic['strategy' + str(send["Symbol"])])

            dic['_action' + str(send["Symbol"])] =\
                market_dic['market' + str(send["Symbol"])].on_market_data_received(send)
            total[str(send["Symbol"])], holdings[str(send["Symbol"])], \
                cash[str(send["Symbol"])], news[str(send["Symbol"])] = \
                market_dic['market' + str(send["Symbol"])].buy_sell_or_hold_something(
                    send, dic['_action' + str(send["Symbol"])])

        if list(news.values()) == [None] * num_to_select:
            pass
        else:
            for i in range(len(list(news.values()))):
                if list(news.values())[i] is not None:
                    print(list(news.keys())[i], ':', list(news.values())[i])
            sum_total = sum(total.values())
            sum_cash = sum(cash.values())
            sum_holdings = sum(holdings.values())
            print('total = %d, holding = %d, cash = %d' %
                  (sum_total, sum_holdings, sum_cash))

    print('---------------------')
    print('final %s total are %d, '
          '\n final %s total are %d, '
          '\n final %s total are %d, \n' %
          (list(total.keys())[0], list(total.values())[0],
           list(total.keys())[1], list(total.values())[1],
           list(total.keys())[2], list(total.values())[2]))
    print('---------------------')
    print('final %s holding are %d, '
          '\n final %s holding are %d, '
          '\n final %s holding are %d, \n' %
          (list(holdings.keys())[0], list(holdings.values())[0],
           list(holdings.keys())[1], list(holdings.values())[1],
           list(holdings.keys())[2], list(holdings.values())[2]))
    print('---------------------')
    print('final %s cash are %d, '
          '\n final %s cash are %d, '
          '\n final %s cash are %d, \n' %
          (list(cash.keys())[0], list(cash.values())[0],
           list(cash.keys())[1], list(cash.values())[1],
           list(cash.keys())[2], list(cash.values())[2]))
