import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

# open, high, low, close, volume

def get_rate(p1, p2):
    return (p2 / p1 - 1) * 100

def process_data(df, interval, number_of_data):
    # features we want to get
    data_avg_price = []
    close_price = []
    close_price_rate = []

    for i in range(interval, len(df)-interval, interval):
        close_price.append(df["close"][i])
        close_price_rate.append(get_rate(df["close"][i-interval], df["close"][i]))
    
    X, y, p = [], [], []
    for i in range(number_of_data, len(close_price_rate)):
        X.append(close_price_rate[i-number_of_data:i-1])
        y.append(close_price_rate[i])
        p.append(close_price[i])
    
    return np.array(X), np.array(y), p

def xgboost_training(X, y, n_estimators, max_depth, alpha, learning_rate):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    model = xgb.XGBRegressor(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate)
    model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)])

    return model

def RSI(period):
    df = pd.read_csv('data.csv')
    close = df.close
    # 日漲跌
    Chg = close - close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    
    # 計算12日平均漲跌幅度
    import numpy as np
    up_mean = []
    down_mean = []
    for i in range(period+1, len(Chg_pos)+1):
        up_mean.append(np.mean(Chg_pos.values[i-period:i]))
        down_mean.append(np.mean(Chg_neg.values[i-period:i]))
    
    # 計算 RSI
    rsi = [0.0 for i in range(period)]
    for i in range(len(up_mean)):
        rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
    rsi_series = pd.Series(data = rsi)
    df['rsi_'+str(period)] = rsi_series
    df.to_csv('data.csv',index=False)
