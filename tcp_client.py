"""
Receives the data from the server and it follows a strategy to make the predictions. There are two strategies available:
* Logistic regression (set strategy = 1)
* Oscillator and bands ensemble strategy (set strategy = 2). Default value.

Based on the predictions, sends a buy, sell or hold order for each one of the different stocks that are being sent.
Makes the following assumptions:
* Always exchanges 10 stocks (buy or sell).
* Initial capital per stock $100000
"""
import socket
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
strategy = 2  # change this value depending on what strategy to use

if strategy == 1:
    import trading_strategy_strategy1 as ts
    import market_actions_strategy1 as ma
else:
    import trading_strategy2 as ts
    import market_actions_strategy2 as ma

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
    for i in range(len(list(total.keys()))):
        print('final', list(total.keys())[i], 'total: $', list(total.values())[i])
    print('---------------------')
    for i in range(len(list(holdings.keys()))):
        print('final', list(holdings.keys())[i], 'holdings: $', list(holdings.values())[i])
    print('---------------------')
    for i in range(len(list(cash.keys()))):
        print('final', list(cash.keys())[i], 'cash: $', list(cash.values())[i])
    print('You made:', sum(total.values()) - num_stocks * 100000)
