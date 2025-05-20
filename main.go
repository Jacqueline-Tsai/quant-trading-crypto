package main
import (
	"fmt"
	"context"
	"strconv"
	"time"
    "github.com/adshao/go-binance/v2"
)

// HelloWorld struct
type HelloWorld struct {
	Message string
}

// HelloWorld method associated with HelloWorld struct
func (h HelloWorld) HelloWorld() {
	fmt.Println("Hello from the HelloWorld method!")
}


func main() {
	h := HelloWorld{}
	h.HelloWorld()

	// const
	var (   
		apiKey = os.Getenv("API_KEY")
		secretKey = os.Getenv("SECRET_KEY")
		
		min_trade_amount = 5.0 //USDT

		// strategy
		mean_period_short = 4
		mean_period_long = 9
		time_period = 40 * time.Second
		sma_buy_threshold = 0.0015
		sma_sell_threshold = 0.002
		trima_buy_threshold = 0.001
		trima_sell_threshold = 0.0005
		stop_loss_amount = 800 //usdt
	)

	// variable
	client := binance.NewClient(apiKey, secretKey)
	asset_present_usdt_amount := 20.0
	asset_present_btc_amount := 0.0
	price_list := make([]float64, 0)
	
	getAccountBalance := func () {
		res, err := client.NewGetAccountService().Do(context.Background())
		if err != nil {
			fmt.Println(err)
			return
		}
		for _, e := range res.Balances {
			free, _ := strconv.ParseFloat(e.Free, 32)
			if e.Asset == "BTC" {
				asset_present_btc_amount := free
			}
			if e.Asset == "USDT" {
				asset_present_usdt_amount := free
			}
		}
		fmt.Println(res)
	}

	listOrder := func () {
		orders, err := client.NewListOrdersService().Symbol("BTCUSDT").Do(context.Background())
		if err != nil {
			fmt.Println(err)
			return
		}
		for _, order := range orders {
			fmt.Println(*order)
		}
	}

	createMarketBuyOrder := func(amount float64) int { //quantity float64, price float64
		order, err := client.NewCreateOrderService().Symbol("BTCUSDT").Side(binance.SideTypeBuy).Type(binance.OrderTypeMarket).Quantity(amount).Do(context.Background())
		if err != nil {
			fmt.Println(err)
			return -1
		}
		fmt.Println(order)
		return 0
	}

	createMarketSellOrder := func(amount float64) int { //quantity float64, price float64
		order, err := client.NewCreateOrderService().Symbol("BTCUSDT").Side(binance.SideTypeSell).Type(binance.OrderTypeMarket).Quantity(amount).Do(context.Background())
		if err != nil {
			fmt.Println(err)
			return -1
		}
		fmt.Println(order)
		return 0
	}

	/*cancelOrder := func (orderId int) {
		_, err := client.NewCancelOrderService().Symbol("BTCUSDT").OrderID(orderId).Do(context.Background())
		if err != nil {
			fmt.Println(err)
			return
		}
	}*/

	getPrice := func () {
		prices, err := client.NewListPricesService().Do(context.Background())
		if err != nil {
			fmt.Println(err)
    			return
		}

		for _, p := range prices {
			if (*p).Symbol == "BTCUSDT" {
				price, _ := strconv.ParseFloat((*p).Price, 64)
				price_list = append(price_list, price)
				return 
			}
		}
		return
	}

	trade := func () {

		mean := func (list[] float64) float64{
			sum := 0.0
			for _, val := range list {
				sum += val
			}
			return sum / float64(len(list))
		}

		rolling_avg := func (originalList[] float64, windowLength int) []float64 {
			result := make([]float64, 0)
			for i:=0; i<=len(originalList)-windowLength; i++ {
				result = append(result, mean(originalList[i:i+windowLength]))
			}
			return result
		}

		getPrice()
		price := price_list[len(price_list)-1]
		getAccountBalance()
		current_asset_value := asset_present_usdt_amount + price * asset_present_btc_amount
		if current_asset_value < stop_loss_amount {
			createMarketSellOrder(asset_present_btc_amount)
		}

		sma5 := rolling_avg(price_list[2*(mean_period_long-mean_period_short)-1:], mean_period_short)
		sma10 := rolling_avg(price_list, mean_period_long)
		trima5 := rolling_avg(sma5, mean_period_short)
		trima10 := rolling_avg(sma10, mean_period_long)

		sma5 = sma5[len(sma5)-2:]
		sma10 = sma10[len(sma10)-2:]
		trima5 = trima5[len(trima5)-2:]

		if asset_present_usdt_amount > min_trade_amount {
		// buy
			if (sma5[0] < sma10[0] && sma5[1] > (sma10[1] * (1+sma_buy_threshold)) && trima5[1] > trima5[0] && trima5[1] > (trima10[0] * (1+trima_buy_threshold))) {
				createMarketBuyOrder(asset_present_usdt_amount/price)
				asset_present_btc_amount += asset_present_usdt_amount/price
				asset_present_usdt_amount -= asset_present_usdt_amount
				fmt.Println(time.Now(), "buy", price, " total btc: ", asset_present_btc_amount)
			}
		}
		
		if asset_present_btc_amount * price > min_trade_amount {
		// sell
			if (sma5[0] > sma10[0] && sma5[1] < (sma10[1] * (1-sma_sell_threshold)) && trima5[1] < trima5[0] && trima5[1] < (trima10[0] * (1-trima_sell_threshold))) {
				createMarketSellOrder(asset_present_btc_amount)
				asset_present_usdt_amount += asset_present_btc_amount * price
				asset_present_btc_amount -= asset_present_btc_amount
				fmt.Println(time.Now(), "sell", price, " total usdt: ", asset_present_usdt_amount)				
			}
		}
	}
	
	getAccountBalance()

	for i:=0; i<mean_period_long*2-1; i++ {
		getPrice()
		time.Sleep(time_period)
	}

	for true {
		price_list = price_list[1:]
		trade()
		time.Sleep(time_period)
	}

	createMarketBuyOrder(0.0005)
	createMarketSellOrder(0.0005)

}
