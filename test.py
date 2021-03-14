import pandas as pd
from create_df import data_to_df
from feature_engineering import features_df
from sklearn.linear_model import LogisticRegression

reader = pd.read_csv('OneDayData.csv')
symbols = list('FB')
num_to_select = 1

class DIRECTION:

    BUY = 1
    SELL = -1
    HOLD = 0

buy = True
sell = False
datetime = list()
_open = list()
high = list()
low = list()
close = list()
volume = list()

high_low = list()
open_close = list()
price = list()
Volatility = list()
momentum = list()
rsi = list()
macd = list()
min5 = list()
min10 = list()
min30 = list()
change = list()
_return = list()
vol_pct_change = list()
y = list()
model = LogisticRegression(solver='lbfgs', random_state=40, max_iter=1000)


def prepare_dataframe(original):
    datetime.append(original['Datetime'])
    _open.append(original['Open'])
    high.append(original['High'])
    low.append(original['Low'])
    close.append(original['Close'])
    volume.append(original['Volume'])
    data_df = data_to_df(datetime, _open, high, low, close, volume)
    return data_df


def getting_features(original):
    data_df = prepare_dataframe(original)
    price_update = features_df(data_df)
    return price_update


def fit(original):

    price_update = getting_features(original)
    price.append(price_update['Close'])
    high_low.append(price_update['High'] - price_update['Low'])
    open_close.append(price_update['Open'] - price_update['Close'])
    Volatility.append(price_update['Volatility'])
    macd.append(price_update['MACD'])
    min5.append(price_update['5min'])
    min10.append(price_update['10min'])
    min30.append(price_update['30min'])
    change.append(price_update['Change'])
    _return.append(price_update['Return'])
    vol_pct_change.append(price_update['volume change_pct'])

    if len(price) > 1:
        if price[len(price) - 1] > price[len(price) - 2]:
            y.append(1)
        else:
            y.append(-1)
    else:
        y.append(-1)

    if len(price) > 40:
        fit_x = pd.DataFrame({'Open-Close': open_close[30:], 'High-Low': high_low[30:],
                              'Volatility': Volatility[30:], 'MACD': macd[30:], '5min': min5[30:],
                              '10min': min10[30:], '30min': min30[30:], 'Change': change[30:],
                              'Return': _return[30:], 'VolChangePct': vol_pct_change[30:]})
        fit_y = pd.DataFrame({'Predictor': y[30:]})
        model.fit(fit_x, fit_y.values.ravel())
        return model


def predict(price_update):
    global buy
    global sell
    if len(price) > 40:
        model = fit(price_update)
        predict_value = model.predict(
            [[price_update['Open'] - price_update['Close'], price_update['High'] - price_update['Low'],
              price_update['Volatility'],  price_update['MACD'],
              price_update['5min'], price_update['10min'], price_update['30min'], price_update['Change'],
              price_update['Return'], price_update['volume change_pct']]])
        if predict_value == 1 and buy:
            sell = True
            buy = False
            print('BUY')
            return DIRECTION.BUY
        elif predict_value == -1 and sell:
            sell = False
            buy = True
            print('SELL')
            return DIRECTION.SELL

N = len(reader[reader['Symbol'] == 'FB'])
for j in range(N):
    for i in range(num_to_select):
        send = reader[reader['Symbol'] == 'FB']
        send = send.iloc[j]
        send = send.to_dict()
        data_df = predict(send)
        print(data_df)