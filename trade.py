import pandas as pd
import numpy as np
import time, math, random
from datetime import datetime

class Trade:
    # const
    brokerage_fee = 0.0006
    overall_stop_loss_point = 800
    min_trade_amount = 0 #USD
    # variable
    current_position = 0
    asset_present_btc_amount = 0
    asset_present_usd_amount = 1000
    current_btc_price = 0   # tmp
    max_asset_value = 1000
    max_drawdown = 0
    #cost_price = 0
    #rate_of_return_freq = [0 for i in range(20)]
    total_cost = 0

    def slippage(self):
        return random.uniform(0, 0.0001)
    def buy(self, amount): #以實際成交價為主
        #print('buy', self.current_btc_price)
        self.asset_present_usd_amount -= amount * (1 + self.brokerage_fee + self.slippage())
        self.asset_present_btc_amount += amount / self.current_btc_price
        self.total_cost += amount
        #self.cost_price = self.current_btc_price
    def sell(self, amount):
        #print('sell', self.current_btc_price)
        self.asset_present_usd_amount += amount * (1 - self.brokerage_fee - self.slippage())
        self.asset_present_btc_amount -= amount / self.current_btc_price
        self.max_asset_value = max(self.max_asset_value, self.get_asset_present_value())
        self.max_drawdown = max(self.max_drawdown, (self.max_asset_value - self.get_asset_present_value())/self.max_asset_value)
    def sell_all(self):
        self.sell(self.current_btc_price * self.asset_present_btc_amount)
    def buy_all(self):
        self.buy(self.asset_present_usd_amount)
    def get_current_btc_price(self): #tmp
        return self.current_btc_price
    def get_asset_present_value(self):
        return self.get_current_btc_price() * self.asset_present_btc_amount + self.asset_present_usd_amount
    def get_prediction(self): #tmp
        # postive for buy, negitive for sell
        return 0
    def backtesting(self, df, action):
        min_asset_value = 1000
        strategy_prices = []
        for i in range(1,len(action)):
            if action[i] == 0: continue
            self.current_btc_price = df['Open'][i+1]
            strategy_prices.append(self.get_asset_present_value())
            if action[i] >= self.min_trade_amount:
                #self.buy(min(self.asset_present_usd_amount, action[i]))
                self.buy_all()
            if action[i] <= -self.min_trade_amount:
                #self.sell(min(self.asset_present_btc_amount * self.current_btc_price, -action[i]))
                self.sell_all()
            min_asset_value = min(min_asset_value, self.get_asset_present_value())
            #if min_asset_value < self.overall_stop_loss_point:
                #print("you're done")
                #break
        self.current_btc_price = df['Open'][len(action)-1]
        self.sell_all()
        
        start_time = datetime.fromtimestamp(df['Open time'][0]/1e3)
        end_time = datetime.fromtimestamp(df['Open time'][len(df)-1]/1e3)
        #start_time = datetime.strptime(' '.join(df['Open time'][0].split('T')).split('+')[0], '%Y-%m-%d %H:%M:%S')
        #end_time = datetime.strptime(' '.join(df['Open time'][len(df)-1].split('T')).split('+')[0], '%Y-%m-%d %H:%M:%S')
        print("============================ RESULT ============================")
        print("Trading Period: ", start_time, '~', end_time)
        print("Final asset value: ", self.get_asset_present_value())
        print('Hold Until End: ', df['Close'][len(df)-1] / df['Close'][0] * 1000)
        print('Internal Rate of Return: ', pow(self.get_asset_present_value()/1000, 365/(end_time-start_time).days))
        print('Max Dropdown: ', self.max_drawdown)
        print('Volatility', self.calculate_volatility(strategy_prices))
        print('Sharpe Ratio', self.calculate_sharpe_ratio(strategy_prices, 0.001))
        print("number of trancations : ", sum([1 if i==1 else 0 for i in action]))
        #print("number of sell : ", sum([1 if i==-1000 else 0 for i in action]))
        #print("rate of return frequency : ", self.rate_of_return_freq)
        
    def calculate_volatility(self, prices):
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns)

    def calculate_sharpe_ratio(self, prices, risk_free_rate_annual):
        returns = np.diff(prices) / prices[:-1]
        risk_free_rate = risk_free_rate_annual / 252
        average_return = np.mean(returns)
        volatility = np.std(returns)
        return (average_return - risk_free_rate) / volatility

