import socket
import trading_strategy as ts
import market_actions as ma
import ast

num_stocks = 2
HOST, PORT = "localhost", 9995
data = "5"
counter = 0
# strategy = ts.Strategy()
# market = ma.MarketActions(strategy)
strategy_dic = {}
market_dic = {}
dic = {}
total = {}
holdings = {}
cash = {}

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "", "utf-8"))

    while True:
        message = []
        received = []
        # accepts messages
        for i in range(num_stocks):
            message.append(str(sock.recv(1024), "utf-8"))

        # creates list of messages for each minute
        for i in range(len(message)):
            element = message[i].split('\n')
            for j in element:
                if len(j) > 65:
                    received.append(j)

        # counter = 0
        # dic = {}

        # applies market actions on each message in list
        for price_update in received:
            counter += 1
            price_update = ast.literal_eval(price_update)

            if counter < (num_stocks + 1):
                print(counter)
                strategy_dic['strategy' + str(price_update["Symbol"])] = ts.Strategy()
                market_dic['market' + str(price_update["Symbol"])] = ma.MarketActions(strategy_dic['strategy' + str(price_update["Symbol"])])
                # locals().update(strategy_dic)
                # locals().update(market_dic)
                print(strategy_dic,'------',market_dic)

            # print(market_dic['market' + str(price_update["Symbol"])])
            # print(price_update["Symbol"])
            dic['_action' + str(price_update["Symbol"])] = market_dic['market' + str(price_update["Symbol"])].on_market_data_received(price_update)
            # total[str(price_update["Symbol"])], \
            # holdings[str(price_update["Symbol"])], \
            # cash[str(price_update["Symbol"])] = market_dic['market' + str(price_update["Symbol"])].buy_sell_or_hold_something(price_update, dic['_action' + str(price_update["Symbol"])])
            print(price_update["Symbol"], market_dic['market' + str(price_update["Symbol"])].buy_sell_or_hold_something(price_update, dic['_action' + str(price_update["Symbol"])]))

            # _action = naive_backtester.on_market_data_received(send)
            # naive_backtester.buy_sell_or_hold_something(send, _action)

            # locals().update(dic)
            # locals().update(total)
            # locals().update(holdings)
            # locals().update(cash)

            # print(price_update["Symbol"])
            # print(dic)
            # print(cash)


            # price_update = ast.literal_eval(price_update)
            # _action = market.on_market_data_received(price_update)
            # market.buy_sell_or_hold_something(price_update, _action)

        # act on the data
        # feed relevant data into model

    # print("Sent:     {}".format(data))
    # print("Received: {}".format(received[0]))
    # print("Received: {}".format(received[1]))
    # print("Received: {}".format(received))

