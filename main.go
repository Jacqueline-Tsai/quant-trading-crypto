package main
import (
	"fmt"
	"context"
	"strconv"
	"time"
    	"github.com/adshao/go-binance/v2"
)

func main() {
	// const
	var (   
		apiKey = "8ablyXVDWrw27SPImVGI0xOd2Tu5vQzpPoA214qQsPvwqEu0ae09MzHgIXVBFyF6"
		secretKey = "4C5rh5t6UqktlTVJgaZs2n5jIVSO537RzFcXlnqi5A7umydV0KsdjCIzlab9Qo1f"
		
		min_trade_amount = 5 //USDT
	)

	// variable
	client := binance.NewClient(apiKey, secretKey)
	asset_present_usdt_amount = 1000
	asset_present_btc_amount = 0	

	createBuyOrder := func(quantity float64, price float64) int {
		order, _ := client.NewCreateOrderService().Symbol("BTCUSDT").Side(binance.SideTypeBuy).Type(binance.OrderTypeLimit).TimeInForce(binance.TimeInForceTypeGTC).Quantity("0.001").Price("20000").Do(context.Background())
		fmt.Println(order)
		return 0//order
	}
	getPrice := func () float64 {
		prices, err := client.NewListPricesService().Do(context.Background())
		if err != nil {
			fmt.Println(err)
    			return -1
		}
		fmt.Println(prices)
		for _, p := range prices {
			fmt.Println(p)
			if (*p).Symbol == "BTCUSDT" {
				price, _ := strconv.ParseFloat((*p).Price, 64)
				return price
			}
		}
		return -1
	}
	trade := func () {
		if asset_present_usdt_amount > min_trade_amount {
			// buying
		}
		
		if asset_present_btc_amount * current_btc_price > min_trade_amount {
			// sell
		}
		fmt.Println("trade")
		fmt.Println(getPrice())
	}
	for true {
		_ = time.AfterFunc(2 * time.Second, trade)
		time.Sleep(2 * time.Second)
	}	
	fmt.Println(createBuyOrder(0.001, 20000))
}
