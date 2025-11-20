# binance_client.py
from binance.client import Client
from binance.enums import *
import pandas as pd

class BinanceAPI:
    def __init__(self, api_key, api_secret, testnet=True):  # Changed default to True
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.testnet = testnet
        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'

    def get_klines(self, symbol="BTCUSDT", interval="15m", limit=100):
        """Fetch historical klines and return list of closing prices"""
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        closes = [float(k[4]) for k in klines]  # closing prices
        print(f"Fetched {len(closes)} klines for {symbol} at interval {interval}")
        return closes

    def place_order(self, symbol, side, quantity, order_type=ORDER_TYPE_MARKET):
        """Execute trade"""
        if self.testnet:
            # Use test order for testnet
            order = self.client.create_test_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
            print(f"TESTNET ORDER: {side} {quantity} {symbol}")
        else:
            # Use real order for live trading
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
            print(f"LIVE ORDER: {side} {quantity} {symbol}")
        return order