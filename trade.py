import pandas as pd
import time, math, random
from datetime import datetime

class Trade:
    # const
    brokerage_fee = 0.001
    overall_stop_loss_point = 800
    min_trade_amount = 1 #USD
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
    def get_current_btc_price(self): #tmp
        return self.current_btc_price
    def get_asset_present_value(self):
        return self.get_current_btc_price() * self.asset_present_btc_amount + self.asset_present_usd_amount
    def get_prediction(self): #tmp
        # postive for buy, negitive for sell
        return 0
    def backtesting(self, df, action):
        min_asset_value = 1000
        for i in range(1,len(action)):
            if action[i] == 0: continue
            self.current_btc_price = df['open'][i+1]
            if action[i] >= self.min_trade_amount:
                self.buy(min(self.asset_present_usd_amount, action[i]))
            if action[i] <= -self.min_trade_amount:
                #self.sell(min(self.asset_present_btc_amount * self.current_btc_price, -action[i]))
                self.sell_all()
            min_asset_value = min(min_asset_value, self.get_asset_present_value())
            if min_asset_value < self.overall_stop_loss_point:
                print("you're done")
                break
        self.current_btc_price = df['open'][len(action)-1]
        self.sell_all()
        
        start_time = datetime.strptime(' '.join(df['startTime'][0].split('T')).split('+')[0], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(' '.join(df['startTime'][len(df)-1].split('T')).split('+')[0], '%Y-%m-%d %H:%M:%S')
        print("Trading Period: ", start_time, '~', end_time)
        print("Final asset value: ", self.get_asset_present_value())
        print('Hold Until End: ', df['close'][len(df)-1] / df['close'][0] * 1000)
        print('Internal Rate of Return: ', pow(self.get_asset_present_value()/1000, 365/(end_time-start_time).days))
        print('Max Dropdown: ', self.max_drawdown)
        #print("number of buy : ", sum([1 if i==1000 else 0 for i in action]))
        #print("number of sell : ", sum([1 if i==-1000 else 0 for i in action]))
        #print("rate of return frequency : ", self.rate_of_return_freq)

