import pandas as pd
from random import sample
import trading_strategy1 as ts1
import trading_strategy2 as ts2
import market_actions_strategy1 as ma1
import market_actions_strategy2 as ma2
from create_one_day_data import create_df
from openpyxl import load_workbook
from datetime import date

number_stocks = 500
today = str(date.today())

data = load_workbook('SPY500.xlsx')
data = data['Sheet1']
data = data.values
columns = next(data)[0:]
df = pd.DataFrame(data, columns=columns)
Symbols = list(df['Symbol'])

lst_stocks = sample(Symbols, number_stocks)
deleted_stocks = ['ALXN', 'MXIM', 'VAR', 'LB', 'COG', 'FLIR']
if number_stocks != 500:
    print('We randomly choose', number_stocks, 'stocks from the SPY 500. \n The chosen stocks are the following:')
    print(lst_stocks)

for element in deleted_stocks:
    if element in lst_stocks:
        print('Deleted', element, '. Symbol may be delisted from yfinance.')
        lst_stocks.remove(element)
num_to_select = len(lst_stocks)

if __name__ == '__main__':

    reader = create_df(str(today), list_stocks=lst_stocks)
    average_price = (reader.mean(axis=0, numeric_only=True))['Close']
    print('\n The mean price of the stocks on', today, 'is', average_price)

    for i in range(2):
        if i == 0:
            print('\n STRATEGY 1 (logistic regression)')
            ts = ts1
            ma = ma1
        else:
            print('STRATEGY 2')
            ts = ts2
            ma = ma2

        strategy_dic = {}
        market_dic = {}
        dic = {}
        total = {}
        holdings = {}
        cash = {}
        news = {}
        symbols = lst_stocks
        counter = 0

        length = []
        for symbol in symbols:
            N = len(reader[reader['Symbol'] == symbol])
            length.append(N)
        N = min(length)

        for j in range(N):
            for symbol in symbols:
                send = reader[reader['Symbol'] == symbol]
                send = send.iloc[j]
                send = send.to_dict()

                counter += 1
                if counter < (num_to_select + 1):
                    strategy_dic['strategy' + str(send["Symbol"])] = ts.Strategy()
                    market_dic['market' + str(send["Symbol"])] = ma.MarketActions(
                        strategy_dic['strategy' + str(send["Symbol"])])

                dic['_action' + str(send["Symbol"])] =\
                    market_dic['market' + str(send["Symbol"])].received_market_data(send)
                total[str(send["Symbol"])], holdings[str(send["Symbol"])], \
                    cash[str(send["Symbol"])], news[str(send["Symbol"])] = \
                    market_dic['market' + str(send["Symbol"])].action_buy_sell_hold(
                        send, dic['_action' + str(send["Symbol"])])

        print('You made: $', sum(total.values()) - num_to_select * 100000)
