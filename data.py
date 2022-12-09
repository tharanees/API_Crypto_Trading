#Run after all sell orders are filled. This calculates the profit on each trade after all sell orders filled and is written on the data.csv file

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
d0 = datetime("FILL IN GMT DATETIME WHEN THE FIRST CRYPTO SELL LIMIT WAS FILLED") 
d1 = datetime.now()

file = open("data.csv")
reader = csv.reader(file)
df = pd.read_csv("data.csv")
n= len(list(reader))-1

for r in range (n):
    coin = str(df.loc[r, 'COIN'])
    trades = client.get_my_trades(symbol=coin)
    tot = 0
    for t in trades:
        dt_object = datetime.fromtimestamp((t["time"]/1000))
        if dt_object >= d0 and dt_object <= d1 and t["isBuyer"] == False:
            tot = tot + ((float(t["quoteQty"])) - (float(t["commission"])))
            df.loc[r, 'sold_date'] = dt_object+timedelta(hours=5, minutes=30)
            df.to_csv("data.csv", index=False)
    df.loc[r, 'sold_for'] = tot
    df.loc[r, 'profit'] = df.loc[r, 'sold_for'] - df.loc[r, 'bought_for']
    df.to_csv("data.csv", index=False)
