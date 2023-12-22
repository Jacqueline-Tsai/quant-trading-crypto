import numpy as np
import pandas as pd
import math
from datetime import datetime
from trade import Trade

# up stage
def method1(history_data, mean_period_short, mean_period_long, period, sma_buy_threshold, sma_sell_threshold, trima_buy_threshold, trima_sell_threshold):
    history_data = history_data[(history_data.index % period == 0)].reset_index()
    sma5 = history_data.Close.rolling(window=mean_period_short).mean()
    trima5 = sma5.rolling(window=mean_period_short).mean()
    sma10 = history_data.Close.rolling(window=mean_period_long).mean()
    trima10 = sma10.rolling(window=mean_period_long).mean()
    sma_dif = sma5 - sma10
    trima_dif = trima5 - trima10

    stock, sma_sig = 0, [0 for i in range(mean_period_long)]
    for i in range(mean_period_long, len(sma_dif)):
        # 5MA往上穿越10MA
        if stock == 0 and sma_dif[i-1] < 0 and sma5[i] > (sma10[i] * (1+sma_buy_threshold)) and trima5[i] > trima5[i-1] and trima5[i] > (trima10[i] * (1+trima_buy_threshold)):
            stock += 1
            sma_sig.append(1)
        # 5MA往下穿越10MA
        elif stock == 1 and sma_dif[i-1] > 0 and sma5[i] < (sma10[i] * (1-sma_sell_threshold)) and trima5[i] < trima5[i-1] and trima5[i] < (trima10[i] * (1-trima_sell_threshold)):
            stock -= 1
            sma_sig.append(-1)
        else:
            sma_sig.append(0)

    trade = Trade()
    trade.backtesting(history_data, pd.Series(sma_sig))

"""
def amount(df):
    #1.abs(df.Close[i-1]-df.low[i])
    #2.abs(df.Close[i-1]-df.high[i])
    #3.df.high[i]-df.low[i]
    atr = [0]
    for i in range(1,len(df)):
        val1 = df.high[i]-df.low[i]
        val2 = abs(df.Close[i-1]-df.low[i])
        val3 = abs(df.Close[i-1]-df.high[i])
        #atr.append(min(tmp * max(max(1, val1), max(val2, val3)), 1000))
    return pd.Series(atr)
"""

data = pd.read_csv('20230110_20231111.csv')
threshold_trail = [0.0005, 0.001, 0.002]
for period in [10, 100]:
    for sma_buy_threshold in threshold_trail:
        for sma_sell_threshold in threshold_trail:
            for trima_buy_threshold in threshold_trail:
                for trima_sell_threshold in threshold_trail:
                    method1(data, 4, 9, period, sma_buy_threshold, sma_sell_threshold, trima_buy_threshold, trima_sell_threshold)
                

#method1(pd.read_csv('20200902_20210415.csv'), 4, 9, 10, 0, 0.001, 0.0005, 0.001)
#method1(pd.read_csv('down_stage_20210502_20210711.csv'), 4, 9, 100, 0.002, 0, 0.002, 0.0005)
#method1(pd.read_csv('down_stage2_20211107_now.csv'), 4, 9, 100, 0.002, 0, 0.002, 0.0005)
