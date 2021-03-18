# day_trading_system

### Authors: [Maggie Wu](https://github.com/MaggieWoo2), [Sambhav Jain](https://github.com/sambhavjain3211) and Ana Ysasi.

Final project for Dr. Sebastien Donadio's Real Time Intelligent Systems course at the University of Chicago's Master of Science in Analytics.

---

## Description:

In this project we simulate a day trading strategy, where we get relevant stock data every minute from a simulated server.

Using the stock data, we calcultate different features to fit it to a logistic regression model. We recalculate the model every time we receive new data. This way we pretend to predict the values of the stocks and buy or sell based on the regression's outputs.

In the visual below, the terminal has real-time stock info by the minute (simulated to speed things up) whereas the console is displaying all buy and sell orders along with total $, which is calculated by adding up holdings + cash. 

![Demo of the code](https://github.com/anapysasi/day_trading_system/blob/main/DEMO.gif)
![](https://github.com/anapysasi/day_trading_system/blob/main/result_sample.png)

---

## Installation Guide

```python
pip3 install gitpython

import os
from git.repo.base import Repo
Repo.clone_from("https://github.com/anapysasi/day_trading_system", "folderToSave")
```

## Quickstart Guide

#### File: `create_one_day_data.py`

This file creates the data needed to run the model. You can choose what day you want to trade. It has to be a day within the last 7 days and the output file will have minute level data for all the stocks in the [S&P 500](https://github.com/anapysasi/day_trading_system/blob/main/SPY500.xlsx) for that particular day<sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup>

#### File: `OneDayData.csv`

Data used to test the model. Corresponds to minute level data from stocks in the S&P 500 for the day **2021-03-09** (day can be altered and set to whatever the user desires).

### Client server :

We use the TCP protocol in the communication of the client-server model. 

#### File: `tcp_server.py`

Sends the data to the client. In order to do so, it needs the client to introduce the number of stocks it wants to trade, lets say <img src="https://render.githubusercontent.com/render/math?math=n">. Since we are simulating how the client-server would work, we randomly select <img src="https://render.githubusercontent.com/render/math?math=n"> stocks and send the minute level data to the client. The data is sent every second for convenience and speed.

#### File: `tcp_client.py`

The client receives the data from the server and it fits it to a regression model to make the predictions. Based on these, it sends a buy, sell, or hold order for each one of the different stocks that are being traded. Assumptions:

* When it buys or sells stocks, it always exchanges <img src="https://render.githubusercontent.com/render/math?math=10"> stocks
* In order to trade with this system the initial capital **per stock** must be <img src="https://render.githubusercontent.com/render/math?math=\$100,000"> (This is an arbitrary number and can be changed fairly easily)

### The following files are used in the model:

#### File: `create_df.py`

The data from the server is sent as dictionaries. Each minute's data for each stock looks like this:

```python
{'Datetime': '2021-03-09 15:59:00-05:00', 'Open': 214.6999969482422, 
       'High': 214.8699951171875, 'Low': 214.42999267578125, 'Close': 214.42999267578125,
       'Volume': 33963, 'Dividends': 0, 'Stock Splits': 0, 'Symbol': 'ECL'}
```

Each feature is converted to individual lists and this file converts these lists into a dataframe to be able to work with them.

#### File `get_all_features.py`

This file chooses the most important features for the logistic regression. It first adds all features calculated in `feature_engineering.py` as new columns to the initial data. Then it fits the model to the logistic regression and gives an importance score for each feature. It runs this for each one of the stock on the S&P 500 and stores this information in a dataframe. At the end in groups by features and it averages the restults. The resulting dataframe is returned with the values ordered from most to less important.

Note that since the logisitc regression has only binary values, the coefficients are both positive and negative. The positive scores indicate a feature that predicts class 1, whereas the negative scores indicate a feature that predicts class 0.

#### File: `feature_engineering.py`

Gets the dataframe from `create_df.py` and it calculates the following features: momentum, relative strength index (RSI), moving average convergence/divergence, volatility, 5, 10, and 30 mins moving average, volume change, percentage volume change, upper and lower bands and z-score.

#### File: `get_all_features.py`

Calculates the most important features for all the 500 stocks. The final features taken in the model are: `min10`, `awesome_oscillator`, `Change`, `daily_log_return`, `Volatility`, `hband_indicator`, `lband_indicator`.

#### File `trading_strategy1.py`

Gets the original data with all the features (`open - close`, `high - low`, `volume`, `price`, `awesome_oscillator`, `daily_log_return`, `change`, `min10`, `hband_indicator`, and `lband_indicator`) and fits a model with it. It uses Logistic Regression to predict if the price the following period is going to be higher or lower than the current period and then makes a decision to buy, sell, or hold. 

#### File `trading_strategy2.py`

Gets the original data with limited features (`awesome_oscillator`, `hband_indicator`, `lband_indicator`) and fits a model with it. It uses an ensemble between the awesome oscillator and the high and low bollinger bands to make a decision to buy, sell, or hold. 

#### File `market_actions1.py`

Is automatically used with `trading_strategy1.py` (when user selects strategy 1) and is responsible for sending an order and calculating the total, the holdings, and the cash.

#### File `market_actions2.py`

Is automatically used with `trading_strategy2.py` (when user selects strategy 2) and is responsible for sending an order and calculating the total, the holdings, and the cash.

---

#### File `use_case.py`

Shows how the program can be used. It trades 100 stocks at the time for the past 7 days.


<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1"  class="footnote-item"><p>Data obtained from this <a href="https://www.slickcharts.com/sp500" title="Title">source</a>. <a href="#fnref1" class="footnote-backref">↩</a></p>
</li>
