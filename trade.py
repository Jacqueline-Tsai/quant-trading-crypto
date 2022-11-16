import random
import pandas as pd
import time

class Trade:
    # const
    brokerage_fee = 0.003
    overall_stop_loss_point = 800
    min_trade_amount = 1 #USD
    max_trade_amount = 15 #USD
    # variable
    current_position = 0
    asset_present_btc_amount = 0
    asset_present_usd_amount = 1000
    current_btc_price = 0   # tmp
    def buy(self, amount): #以實際成交價為主
        #print('buy', amount)
        self.asset_present_usd_amount -= amount * (1 + self.brokerage_fee)
        self.asset_present_btc_amount += amount / self.current_btc_price
    def sell(self, amount):
        #print('sell', amount)
        self.asset_present_usd_amount += amount * (1 - self.brokerage_fee)
        self.asset_present_btc_amount -= amount / self.current_btc_price
    def get_current_btc_price(self): #tmp
        return self.current_btc_price
    def get_asset_present_value(self):
        return self.get_current_btc_price() * self.asset_present_btc_amount + self.asset_present_usd_amount
    def get_prediction(self):
        # postive for buy, negitive for sell
        rand_num = random.random()
        if rand_num<0.001:
            return random.uniform(self.min_trade_amount, self.max_trade_amount)
        elif rand_num>0.999:
            return -random.uniform(self.min_trade_amount, self.max_trade_amount)
        return 0
    def backtesting(self):
        df = pd.read_csv('./data.csv')
        min_asset_value = 1000
        for i in range(1, len(df.index)):
            self.current_btc_price = (df["open"][i] + df["close"][i]) / 2
            current_btc_price = self.get_current_btc_price()
            action = self.get_prediction()
            if action > self.min_trade_amount:
                self.buy(min(self.asset_present_usd_amount, action))
            if action < -self.min_trade_amount:
                self.sell(min(self.asset_present_btc_amount * current_btc_price, -action))
            min_asset_value = min(min_asset_value, self.get_asset_present_value())
            if min_asset_value < self.overall_stop_loss_point:
                print("you're done")
                break
        print("result : ",self.get_asset_present_value())        
        print("min asset value : ", min_asset_value)
#df = df.set_axis(['startTime', 'time', 'open', 'high', 'low', 'close', 'volume'], axis=1).drop([0])

trade = Trade() 
trade.backtesting()