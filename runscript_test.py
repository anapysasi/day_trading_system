import pandas as pd
import trading_strategy as ts
import market_actions as ma
import tcp_client as client

if __name__ == '__main__':
    strategy = ts.Strategy()
    market = ma.MarketActions(strategy)

    while True:
        received = client.run_client()
        received = received.to_dict()
        _action = market.on_market_data_received(received)
        market.buy_sell_or_hold_something(received, _action)
