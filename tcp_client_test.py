import socket
import trading_strategy as ts
import market_actions as ma
import ast

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
        if not message:
            print('Client received no data: closing socket')
            sock.close()
            break
        else:
            # creates list of messages for each minute
            for i in range(len(message)):
                element = message[i].split('\n')
                for j in element:
                    if len(j) > 65:
                        received.append(j)

        # applies market actions on each message in list
        for price_update in received:
            price_update = ast.literal_eval(price_update)
            _action = market.on_market_data_received(price_update)
            market.buy_sell_or_hold_something(price_update, _action)

        # act on the data
        # feed relevant data into model

    # print("Sent:     {}".format(data))
    # print("Received: {}".format(received[0]))
    # print("Received: {}".format(received[1]))
    # print("Received: {}".format(received))

