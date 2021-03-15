import socket
import trading_strategy as ts
import market_actions as ma
import json

num_stocks = 3
HOST, PORT = "localhost", 9995
data = "5"
strategy = ts.Strategy()
market = ma.MarketActions(strategy)

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
        print(message)
        # creates list of messages for each minute
        for updates in message:
            try:
                received.append(json.loads(updates))
            except:
                split_string = updates.split('\n')
                for j in split_string:
                    received.append(j)
        print(received)
        # applies market actions on each message in list
        for price_update in received:
            _action = market.on_market_data_received(price_update)
            market.buy_sell_or_hold_something(price_update, _action)

        # act on the data
        # feed relevant data into model

    # print("Sent:     {}".format(data))
    # print("Received: {}".format(received[0]))
    # print("Received: {}".format(received[1]))
    # print("Received: {}".format(received))

