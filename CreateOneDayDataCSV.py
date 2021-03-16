import pandas as pd
import yfinance as yf
from openpyxl import load_workbook

data = load_workbook('/Users/anaysasi/Documents/UchicagoCourses/Winter2021/RealTimeIntSystems/Python/FinalProject/SPY500.xlsx')
data = data['Sheet1']
data = data.values
columns = next(data)[0:]

df = pd.DataFrame(data, columns=columns)
Symbols = df['Symbol']

i = 0
data0 = yf.Ticker(Symbols[i])

# You can only choose one day within the last 7 days.
# The format must be 'YYYY-MM-DD'
day = '2021-03-16'
df0 = data0.history(day, interval = '1m')
df0['Symbol'] = [Symbols[i]]*df0.shape[0]

for i in range(1,len(Symbols)):
    data = yf.Ticker(Symbols[i])
    print(i, Symbols[i])
    df = data0.history(day, interval = '1m')
    df['Symbol'] = [Symbols[i]]*df.shape[0]
    df0 = df0.append(df)

df0.head()

# df0.to_csv('OneDayData.csv')