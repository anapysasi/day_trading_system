import pandas as pd
import feature_engineering as fe
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score as acc
from mlxtend.feature_selection import SequentialFeatureSelector as sfs

aapl = pd.read_csv('AAPL.csv')
adbe = pd.read_csv('ADBE.csv')
aes = pd.read_csv('AES.csv')
fb = pd.read_csv('FB.csv')
hal = pd.read_csv('HAL.csv')
intc = pd.read_csv('INTC.csv')
ip = pd.read_csv('IP.csv')
ldos = pd.read_csv('LDOS.csv')
pfe = pd.read_csv('PFE.csv')
stz = pd.read_csv('STZ.csv')


def features_df(stocks):

    stocks['Return'] = round(stocks['Close'] / stocks['Open'] - 1, 3)
    stocks['Change'] = (stocks.Close - stocks.Close.shift(1)).fillna(0)
    stocks['Volatility'] = stocks.Close.ewm(21).std()
    stocks['5min'] = stocks.Close.rolling(5).mean()
    stocks['10min'] = stocks.Close.rolling(10).mean()
    stocks['30min'] = stocks.Close.rolling(30).mean()
    stocks['volume change'] = (stocks.Volume - stocks.Volume.shift(1)).fillna(0)
    stocks['volume change_pct'] = stocks['volume change']/stocks['Volume']
    stocks['Momentum'] = fe.momentum(stocks.Close, 3)
    stocks['RSI'] = fe.rsi(stocks)
    stocks['MACD'], stocks['MACD_Signal'] = fe.macd(stocks)
    return stocks


all_stocks = [aapl, adbe, aes, fb, hal, intc, ip, ldos, pfe, stz]

for index, symbol in enumerate(all_stocks):
    all_stocks[index] = features_df(symbol)

#fit_x = pd.DataFrame({'Open-Close': self.open_close[30:], 'High-Low': self.high_low[30:],
#                                  'Volatility': self.Volatility[30:], 'RSI': self.rsi[30:],
#                                  'Momentum': self.momentum[30:], 'MACD': self.macd[30:], '5min': self.min5[30:],
#                                  '10min': self.min10[30:], '30min': self.min30[30:], 'Change': self.change[30:],
#                                  'Return': self._return[30:], 'VolChangePct': self.vol_pct_change[30:]})
#            fit_y = pd.DataFrame({'Predictor': self.y[30:]})
featured = []
for index, symbol in enumerate(all_stocks):
    symbol['Open-Close'] = symbol['Open'] - symbol['Close']
    symbol['High-Low'] = symbol['High'] - symbol['Low']
    symbol['Predictor'] = symbol['Close'].diff().fillna(0)
    symbol['Predictor'] = symbol['Predictor'].apply(lambda x: 1 if x > 0 else -1)
    symbol = symbol[30:]
    del symbol['Open'], symbol['Close'], symbol['High'], symbol['Low'], symbol['Dividends'], symbol['Volume'], symbol[
        'Stock Splits'], symbol['volume change'], symbol['MACD_Signal'], symbol['Datetime'], symbol['Symbol']
    featured.append(symbol)



# Evaluating features
# Use one of the stocks from all_stocks to check feature importance

df = featured[0]
print(df)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    df.values[:, :-1],
    df.values[:, -1:],
    test_size=0.25,
    random_state=42)

y_train=y_train.astype('int')
y_test=y_test.astype('int')
y_train = y_train.ravel()
y_test = y_test.ravel()


print('Training dataset shape:', X_train.shape, y_train.shape)
print('Testing dataset shape:', X_test.shape, y_test.shape)

# Build RF classifier to use in feature selection
clf = RandomForestClassifier(n_estimators=100, n_jobs=1)

# Build step forward feature selection
sfs1 = sfs(clf,
           k_features=5,
           forward=True,
           floating=False,
           verbose=2,
           scoring='accuracy',
           cv=5)

# Perform SFFS
sfs1 = sfs1.fit(X_train, y_train)

# Which features?
feat_cols = list(sfs1.k_feature_idx_)
print(feat_cols)

# df.to_csv('featured.csv')

