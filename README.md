# day_trading_system

### Authors: [Maggie Wu](https://github.com/MaggieWoo2), [Sambhav Jain](https://github.com/sambhavjain3211) and Ana Ysasi.

Final project for Dr. Sebastien Donadio's Real Time Intelligent Systems course at the University of Chicago's Master of Science in Analytics.

---

## Description:

In this project we simulate a day trading stragety, in which we are getting the data every minute from a server.

Using this data, we calcultate different features to fit it to a regression model. We recalculate the model every time we receive new data. This way we pretend to predit the values of the stocks and buy or sell when is most convenient.

---

## Instalation Guide

```python
pip3 install gitpython

import os
from git.repo.base import Repo
Repo.clone_from("https://github.com/anapysasi/day_trading_system", "folderToSave")
```

## Quickstart Guide

#### File: `CreateOneDayDataCSV.py`

This file creates the data needed to run the model. You can choose what day you want to trade. It has to be a day within the last 7 days and it will take the minute data for all the stocks in the [S&P 500](https://github.com/anapysasi/day_trading_system/blob/main/SPY500.xlsx)<sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup>

#### File: `OneDayData.csv`

Data used to test the model. Corresponds to minute the data from stocks in the S&P 500 for the day **2021-03-09**.

### Client server :

We use the TCP protocol in the communication of the client-server model. 

#### File: `tcp_server.py`

Sends the data to the client. In order to do so, it needs the client to introduce the number of stocks it wants to trade, lets say <img src="https://render.githubusercontent.com/render/math?math=n">. Since we are simulating how the client-server would work, we randomly select <img src="https://render.githubusercontent.com/render/math?math=n"> stocks and send the minute data to the client. The data is sent by minute.

#### File: `tcp_client.py`

The client receives the data from the server and it fits it to a model to make the predictions. Based on these, it sends a buy, sell or hold order for each one of the different stocks that are being trade. Assumptions:

* When it buys or sells stocks, it always exchanges <img src="https://render.githubusercontent.com/render/math?math=10"> sotcks.
* In order to trade with this system the initial capital **per stock** must be <img src="https://render.githubusercontent.com/render/math?math=\$100,000">

### The following files are used in the model:

#### File: `create_df.py`

The data from the server is send as dictionaries. It looks something like this:

```python
{'Datetime': '2021-03-09 15:59:00-05:00', 'Open': 214.6999969482422, 'High': 214.8699951171875, 'Low': 214.42999267578125, 'Close': 214.42999267578125, 'Volume': 33963, 'Dividends': 0, 'Stock Splits': 0, 'Symbol': 'ECL'}
```

These are converted to individual lists and this file converts these lists into a dataframe.

#### File: `feature_engineering.py`

Gets the dataframe from `create_df.py` and it calculates the following features: momentum, relative strength index (RSI), moving average convergence/divergence, volatility, 5-10 and 30 mins moving average, volume change, percentage volume change, upper and lower bands and z-score.

#### File `trading_strategy.py`

Gets the data and fits a model with it. It also predits the following value using said model and decides wheter if it holds, buy or sell.

#### File: `market_actions.py`

Depending on the output from `trading_strategy.py` sends to order and calculates the total, holdings and the cash.

<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1"  class="footnote-item"><p>Data obtained from this <a href="https://www.slickcharts.com/sp500" title="Title">source</a>. <a href="#fnref1" class="footnote-backref">↩</a></p>
</li>
