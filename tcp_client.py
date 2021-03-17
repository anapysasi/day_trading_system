"""
Receives the data from the server and it fits it to a regression model to make the predictions.
Based on the predictions, sends a buy, sell or hold order for each one of the different stocks that are being sent.

Makes the following assumptions:
* Always exchanges 10 stocks (buy or sell).
* Initial capital per stock $100000
"""
import socket
import trading_strategy as ts
import market_actions as ma
import ast

HOST, PORT = "localhost", 9995
data = "5"
counter = 0
strategy_dic = {}
market_dic = {}
dic = {}
total = {}
holdings = {}
cash = {}
news = {}

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "", "utf-8"))
    num_stocks = int(str(sock.recv(1024), "utf-8"))
    print('Number of Stocks trading on:', num_stocks)
    loop_length = int(str(sock.recv(1024), "utf-8"))

    while True:
        message = []
        received = []
        loop_length -= 1
        # accepts messages
        if loop_length == 0:
            print('End of trading day: closing connection')
            sock.close()
            break
        else:
            for i in range(num_stocks):
                message.append(str(sock.recv(1024), "utf-8"))
            # creates list of messages for each minute
            for i in range(len(message)):
                element = message[i].split('\n')
                for j in element:
                    if len(j) > 65:
                        received.append(j)

        # applies market actions on each message in list
        # We need to create as much markets (and actions) as stocks we have.
        for price_update in received:
            counter += 1
            price_update = ast.literal_eval(price_update)

            if counter < (num_stocks + 1):
                strategy_dic['strategy' + str(price_update["Symbol"])] = ts.Strategy()
                market_dic['market' + str(price_update["Symbol"])] = ma.MarketActions(
                    strategy_dic['strategy' + str(price_update["Symbol"])])

            dic['_action' + str(price_update["Symbol"])] = market_dic[
                'market' + str(price_update["Symbol"])].received_market_data(price_update)
            total[str(price_update["Symbol"])], holdings[str(price_update["Symbol"])], cash[
                str(price_update["Symbol"])], news[str(price_update["Symbol"])] = market_dic[
                'market' + str(price_update["Symbol"])].action_buy_sell_hold(
                price_update, dic['_action' + str(price_update["Symbol"])])

        if list(news.values()) == [None] * num_stocks:
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
    print('You made:', sum(total.values()) - num_stocks * 100000)
