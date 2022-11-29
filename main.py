import numpy as np
import pandas as pd
import math
from trade import Trade
from generate_model import xgboost_training, process_data, RSI

def sma(df, period1, period2):
    sma5 = df.close.rolling(window=period1).mean()
    sma10 = df.close.rolling(window=period2).mean()
    sma_dif = sma5 - sma10

    stock, sma_sig = 0, [0 for i in range(period2)]
    for i in range(period2, len(sma_dif)):
        # 5MA往上穿越10MA
        if sma_dif[i-1] < 0 and sma_dif[i] > 0 and stock == 0 and  sma5[i] > (sma10[i] * 1.00):
            stock += 1
            sma_sig.append(1)
        # 5MA往下穿越10MA
        elif sma_dif[i-1] > 0 and sma_dif[i] < 0 and stock == 1:
            stock -= 1
            sma_sig.append(-1)
        else:
            sma_sig.append(0)
    
    return pd.Series(sma_sig)


def dema(df, period1, period2):
    ema5 = df.close.ewm(span=period1, adjust=False).mean()
    dema5 = 2*ema5 - ema5.ewm(span=period1, adjust=False).mean()
    ema10 = df.close.ewm(span=period2, adjust=False).mean()
    dema10 = 2*ema10 - ema10.ewm(span=period2, adjust=False).mean()
    dema_dif = dema5 - dema10

    stock, dema_sig = 0, [0 for i in range(period2)]
    for i in range(period2, len(dema_dif)):
        # 5MA往上穿越10MA
        if dema_dif[i-1] < 0 and dema_dif[i] > 0 and stock == 0 and dema5[i] > dema5[i-1] and dema5[i] > (dema10[i] * 1.003):
            stock += 1
            dema_sig.append(1)
        # 5MA往下穿越10MA
        elif dema_dif[i-1] > 0 and dema_dif[i] < 0 and stock == 1:
            stock -= 1
            dema_sig.append(-1)
        else:
            dema_sig.append(0)

    return pd.Series(dema_sig)
    

def trima(df, period1, period2):
    sma5 = df.close.rolling(window=period1).mean()
    trima5 = sma5.rolling(window=period1).mean()
    sma10 = df.close.rolling(window=period2).mean()
    trima10 = sma10.rolling(window=period2).mean()
    trima_dif = trima5 - trima10

    stock, trima_sig = 0, [0 for i in range(period2)]
    for i in range(period2, len(trima_dif)):
        # 5MA往上穿越10MA
        if trima_dif[i-1] < 0 and trima_dif[i] > 0 and stock == 0 and trima5[i] > trima5[i-1] and trima5[i] > (trima10[i] * 1.00):
            stock += 1
            trima_sig.append(1)
        # 5MA往下穿越10MA
        elif trima_dif[i-1] > 0 and trima_dif[i] < 0 and stock == 1:
            stock -= 1
            trima_sig.append(-1)
        else:
            trima_sig.append(0)
    
    return pd.Series(trima_sig)

def amount(df):
    #1.abs(df.close[i-1]-df.low[i])
    #2.abs(df.close[i-1]-df.high[i])
    #3.df.high[i]-df.low[i]
    atr = [0]
    for i in range(1,len(df)):
        val1 = df.high[i]-df.low[i]
        val2 = abs(df.close[i-1]-df.low[i])
        val3 = abs(df.close[i-1]-df.high[i])
        atr.append(min(70 * max(max(1, val1), max(val2, val3)), 1000))
        #atr.append(1000)
    return pd.Series(atr)


history_data = pd.read_csv('data.csv')
trade = Trade()
trade.backtesting(sma(history_data, 4, 7) * amount(history_data))
# + dema(history_data, 4, 7) * amount(history_data) + trima(history_data, 4, 7) * amount(history_data)
