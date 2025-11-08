# trader.py
import time
from binance.enums import SIDE_BUY, SIDE_SELL
from .binanceapi import BinanceAPI
from .Signal import IndicatorGenerator,Signal


class Trader:
    def __init__(self, api_key, api_secret, symbol="BTCUSDT", interval="15m", quantity=0.001):
        self.symbol = symbol
        self.interval = interval
        self.quantity = quantity
        self.api = BinanceAPI(api_key, api_secret, testnet=True)  # Set testnet=False for live
        self.position = None  # None, "LONG", or "SHORT"

    def fetch_and_analyze(self):
        prices = self.api.get_klines(symbol=self.symbol, interval=self.interval, limit=100)
        indicators = IndicatorGenerator(prices, period=14).generate_signals()

        # extract key indicator values
        rsi = next((s.value for s in indicators if s.name == "RSI"), None)
        ema = next((s.value for s in indicators if s.name == "EMA"), None)
        sma = next((s.value for s in indicators if s.name == "SMA"), None)
        last_price = prices[-1]

        print(f"Current Price: {last_price} | RSI: {rsi} | EMA: {ema} | SMA: {sma}")

        # --- Trading Logic ---
        if rsi is None or ema is None:
            return

        # Basic example strategy
        if rsi < 30 and last_price > ema and self.position != "LONG":
            print("🟢 Buy Signal Detected!")
            self.api.place_order(self.symbol, SIDE_BUY, self.quantity)
            self.position = "LONG"

        elif rsi > 70 and last_price < ema and self.position == "LONG":
            print("🔴 Sell Signal Detected!")
            self.api.place_order(self.symbol, SIDE_SELL, self.quantity)
            self.position = None

    def run(self, sleep_seconds=900):
        """Run every given interval (e.g., every 15 min)"""
        print(f"Starting trader for {self.symbol} on interval {self.interval} ...")
        while True:
            try:
                self.fetch_and_analyze()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(sleep_seconds)
