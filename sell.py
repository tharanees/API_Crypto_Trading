#Run this once all buy orders are filled. It places limit sell orders for the cryptos purchased with a pre-set profit percentage.

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import csv
import pandas as pd
import math
from datetime import datetime,timedelta

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

api_key = "FILL IN YOUR API KEY"
api_secret = "FILL IN YOUR API SECRET CODE"
client = Client(api_key, api_secret)

file = open("data.csv")
reader = csv.reader(file)
df = pd.read_csv("data.csv")
n= len(list(reader))-1

# datetime(year, month, day, hour, minute, second, microsecond)
d0 = datetime("FILL IN GMT DATETIME WHEN THE FIRST CRYPTO BUY LIMIT WAS FILLED") 
d1 = datetime.now()

for r in range (n):
    coin = str(df.loc[r, 'COIN'])
    trades = client.get_my_trades(symbol=coin)
    tot = 0
    tot1 = 0
    for t in trades:
        dt_object = datetime.fromtimestamp((t["time"]/1000))
        if dt_object >= d0 and dt_object <= d1 and t["isBuyer"] == True:
            tot = tot + (float(t["quoteQty"]))
            tot1 = tot1 + ((float(t["qty"])) - (float(t["commission"])))
    df.loc[r, 'bought_for'] = tot
    df.loc[r, 'QTY'] = tot1
    df.loc[r, 'BUY_RATE'] = tot/tot1
    df.to_csv("data.csv", index=False)


for r in range (n):
    coin = str(df.loc[r, 'COIN'])
    sell_qty = round_down(df.loc[r, 'QTY'],int(df.loc[r, 'DP2']))
    df.loc[r, 'QTY'] = sell_qty
    df.to_csv("data.csv", index=False)

    qty = round((df.loc[r, 'QTY']),int(df.loc[r, 'DP2']))
    #placing sell order for all coins bought with a profit margin of 3.5%
    df.loc[r, 'SOLD_RATE'] = round_up((1.035*(df.loc[r, 'BUY_RATE'])),int(df.loc[r, 'DP1']))
    df.loc[r, 'REMAINING'] = df.loc[r, 'bought_for'] - (df.loc[r, 'QTY']*(df.loc[r, 'BUY_RATE']))
    df.to_csv("data.csv", index=False)
    sell_rate = df.loc[r, 'SOLD_RATE']
    #place sell limit order
    sell_limit  = client.order_limit_sell(symbol=coin, quantity=qty, price=sell_rate)


