"""
This file is used to calculate what are the most important features of the model.
The importance coefficient of each one is printed in a dataframe at the end of the program.
This coefficient will be an average of all the stocks.
"""
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.momentum import PercentagePriceOscillator
from ta.trend import macd
from ta.momentum import awesome_oscillator
from ta.others import daily_return
from ta.volatility import BollingerBands
from sklearn.linear_model import LogisticRegression
import yfinance as yf
from openpyxl import load_workbook

# You need to choose what day you want to check.
day = 'YYYY-MM-DD'

data = load_workbook('SPY500.xlsx')
data = data['Sheet1']
data = data.values
columns = next(data)[0:]
df = pd.DataFrame(data, columns=columns)
Symbols = df['Symbol']
lst = []

for k in range(500):
    if k == 344:  # This index gives an error when fitting the model
        pass
    else:
        print(k, Symbols[k])
        data = yf.Ticker(Symbols[k])
        reader = data.history(day, interval='1m')

        y = np.where(reader['Close'].shift(-1) > reader['Close'], 1, -1)[30:]
        reader['rsi_vals'] = RSIIndicator(close=reader.Close, window=10).rsi()
        reader['macd_vals'] = macd(reader.Close, window_slow=26, window_fast=12)
        reader['Ppo'] = PercentagePriceOscillator(reader.Close, window_slow=26, window_fast=12).ppo()
        reader['awesome_oscillator'] = awesome_oscillator(reader.High, reader.Low, window1=5, window2=29)
        reader['daily_log_return'] = daily_return(close=reader.Close)
        reader['Return'] = round(reader['Close'] / reader['Open'] - 1, 3)
        reader['Change'] = (reader.Close - reader.Close.shift(1)).fillna(0)
        reader['Volatility'] = reader.Close.ewm(21).std()
        reader['min5'] = reader.Close.rolling(5).mean()
        reader['min10'] = reader.Close.rolling(10).mean()
        reader['min30'] = reader.Close.rolling(30).mean()
        reader['hband_indicator'] = BollingerBands(close=reader.Close).bollinger_hband_indicator()
        reader['lband_indicator'] = BollingerBands(close=reader.Close).bollinger_lband_indicator()
        reader['Corr'] = reader.Close.rolling(window=10).corr(reader['min10'])

        reader = reader.drop(reader.index[range(30)], axis=0)
        X = reader[['Open', 'High', 'Low', 'Close', 'rsi_vals', 'macd_vals', 'Ppo', 'awesome_oscillator',
                    'daily_log_return', 'Return', 'Change', 'Volatility', 'min5', 'min10',
                    'min30', 'hband_indicator', 'lband_indicator', 'Corr']]

        # define the model
        model = LogisticRegression(solver='lbfgs', random_state=0, max_iter=4000)
        # fit the model
        model.fit(X, y)
        # get importance
        importance = model.coef_[0]
        # summarize feature importance
        for i, v in enumerate(importance):
            if abs(v) > 0.1:
                lst.append([Symbols[k], X.columns[i], abs(v)])

df = pd.DataFrame(lst, columns=["Symbol", "Feature", "coefficient"])
print(len(Symbols))
df = df.groupby('Feature').mean().reset_index(drop=False)
df = df.sort_values(by=['coefficient'], ascending=False)
print(df)
