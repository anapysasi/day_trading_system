# day_trading_system

### Authors: [Maggie Wu](https://github.com/MaggieWoo2), [Sambhav Jain](https://github.com/sambhavjain3211) and Ana Ysasi.

Final project for Dr. Sebastien Donadio's Real Time Intelligent Systems course at the University of Chicago's Master of Science in Analytics.

---

### Description:

In this project we simulate a day trading stragety, in which we are getting the data every minute from a server which is providing the data. We calcultate different features from the data and fit it to a regression model every time we receive a data. This way we pretend to predit the values of the stocks and buy or sell when is most convenient.

---

### Instalation Guide

```python
pip3 install gitpython

import os
from git.repo.base import Repo
Repo.clone_from("https://github.com/anapysasi/day_trading_system", "folderToSave")
```

### Quickstart Guide

#### File: `CreateOneDayDataCSV.py`

This file creates the data needed to run the model. You can choose what day you want to trade. It has to be a day within the last 7 days. It will take the minute data for all the stocks in the [S&P 500](https://github.com/anapysasi/day_trading_system/blob/main/SPY500.xlsx) prueba,<sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup>

#### File: `OneDayData.csv`

A data

#### File: `create_df.py`



#### File: `feature_engineering.py`



#### File: `market_actions.py`



#### File: `tcp_client.py`



#### File: `tcp_server.py`



#### File `trading_strategy.py`



<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1"  class="footnote-item"><p>Here is the footnote. <a href="#fnref1" class="footnote-backref">↩</a></p>
</li>
