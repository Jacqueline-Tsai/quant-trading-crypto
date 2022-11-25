import pandas as pd
import time, math

class Trade:
    # const
<<<<<<< Updated upstream
    brokerage_fee = 0
=======
    brokerage_fee = 0.0015
>>>>>>> Stashed changes
    overall_stop_loss_point = 800
    min_trade_amount = 1 #USD
    max_trade_amount = 15 #USD
    # variable
    current_position = 0
    asset_present_btc_amount = 0
    asset_present_usd_amount = 1000
    current_btc_price = 0   # tmp
<<<<<<< Updated upstream

    cost_price = 0
    rate_of_return_freq = [0 for i in range(20)]
=======
    # rsi variable
    short_tern_pos = 0 
>>>>>>> Stashed changes
    def buy(self, amount): #以實際成交價為主
        #print('buy', self.current_btc_price)
        self.asset_present_usd_amount -= amount * (1 + self.brokerage_fee)
        self.asset_present_btc_amount += amount / self.current_btc_price
        self.cost_price = self.current_btc_price
    def sell(self, amount):
        #print('sell', self.current_btc_price)
        self.asset_present_usd_amount += amount * (1 - self.brokerage_fee)
        self.asset_present_btc_amount -= amount / self.current_btc_price
        if self.cost_price!=0: self.rate_of_return_freq[math.floor((self.current_btc_price/self.cost_price - 1)*100)] += 1
    def sell_all(self):
        self.sell(self.current_btc_price * self.asset_present_btc_amount)
    def get_current_btc_price(self): #tmp
        return self.current_btc_price
    def get_asset_present_value(self):
        return self.get_current_btc_price() * self.asset_present_btc_amount + self.asset_present_usd_amount
    def get_prediction(self): #tmp
        # postive for buy, negitive for sell
        return 0
    def backtesting(self, action):
        df = pd.read_csv('data.csv').reset_index(drop=True)
        min_asset_value = 1000
        for i in range(1,len(action)):#3949013, 5217470
            if action[i] == 0: continue
            self.current_btc_price = df['open'][i+1]
            if action[i] >= self.min_trade_amount:
                self.buy(min(self.asset_present_usd_amount, action[i]))
            if action[i] <= -self.min_trade_amount:
                self.sell(min(self.asset_present_btc_amount * self.current_btc_price, -action[i]))
            min_asset_value = min(min_asset_value, self.get_asset_present_value())
            if min_asset_value < self.overall_stop_loss_point:
                print("you're done")
                break
        self.current_btc_price = df['open'][len(action)-1]
        self.sell_all()
        print("final asset value : ", self.get_asset_present_value())
        print("min asset value : ", min_asset_value)
<<<<<<< Updated upstream
        print("number of buy : ", sum([1 if i==1000 else 0 for i in action]))
        print("number of sell : ", sum([1 if i==-1000 else 0 for i in action]))
        print("rate of return frequency : ", self.rate_of_return_freq)
=======
>>>>>>> Stashed changes

