from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import requests
import pandas as pd
import math
import csv

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

api_key = ""
api_secret = ""
client = Client(api_key, api_secret)


Number = int(input("ENTER NUMBER OF COINS TO BUY"))
file = open("data.csv")
df = pd.read_csv("data.csv")
for count in range (Number):
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    data = response.json()
    coin=input("ENTER COIN: ")
    flag = "NO"
    while flag == "NO":
        try:
            c=0
            while data["symbols"][c]["symbol"] != coin:
                c+=1
            flag = "YES"
        except:
            print("WRONG TICKER")
            coin=input("RE-ENTER COIN: ")

    price = float(data["symbols"][c]["filters"][0]["tickSize"])
    dp1 = 0
    while price != 1:
        dp1 +=1
        price =  price*10

    qty = float(data["symbols"][c]["filters"][2]["stepSize"])
    dp2 = 0
    while qty != 1:
        dp2 +=1
        qty =  qty*10

    r = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol=coin))
    results = r.json()
    frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                             dtype=float)
          for side in ["bids", "asks"]}

    buy_price = frames["asks"].price.min()
    buy_price = round((buy_price-(10*float(data["symbols"][c]["filters"][0]["tickSize"]))),dp1)
    qty = round_up((float(40)/buy_price),dp2)#buy each coin for $40
    df.loc[count, 'COIN'] = coin
    df.loc[count, 'DP1'] = dp1
    df.loc[count, 'DP2'] = dp2
    df.to_csv("data.csv", index=False)

    buy_limit  = client.order_limit_buy(symbol=coin, quantity=qty, price=buy_price)

