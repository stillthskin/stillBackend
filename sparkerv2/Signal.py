import numpy as np

class Signal:
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Signal(name={self.name}, value={self.value})"

class IndicatorGenerator:
    def __init__(self, prices, period=14):
        self.prices = np.array(prices)
        self.period = period

    def sma(self):
        sma_value = np.mean(self.prices[-self.period:])
        return Signal("SMA", round(sma_value, 4))

    def ema(self, span=None):
        if span is None:
            span = self.period
        prices = self.prices
        k = 2 / (span + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * k + ema
        return ema

    def rsi(self):
        deltas = np.diff(self.prices)
        ups = deltas.clip(min=0)
        downs = -deltas.clip(max=0)
        avg_gain = np.mean(ups[-self.period:])
        avg_loss = np.mean(downs[-self.period:])
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi_value = 100 - (100 / (1 + rs))
        return Signal("RSI", round(rsi_value, 2))

    def macd(self):
        ema12 = self.ema(span=12)
        ema26 = self.ema(span=26)
        macd_line = ema12 - ema26
        signal_line = self.ema(span=9)
        histogram = macd_line - signal_line
        return [
            Signal("MACD_Line", round(macd_line, 4)),
            Signal("Signal_Line", round(signal_line, 4)),
            Signal("MACD_Histogram", round(histogram, 4))
        ]

    def bollinger_bands(self):
        sma = np.mean(self.prices[-self.period:])
        std = np.std(self.prices[-self.period:])
        upper = sma + 2 * std
        lower = sma - 2 * std
        return [
            Signal("Bollinger_Upper", round(upper, 4)),
            Signal("Bollinger_Middle", round(sma, 4)),
            Signal("Bollinger_Lower", round(lower, 4))
        ]

    def stochastic(self):
        low = np.min(self.prices[-self.period:])
        high = np.max(self.prices[-self.period:])
        close = self.prices[-1]
        k = 100 * (close - low) / (high - low)
        return Signal("Stochastic_%K", round(k, 2))

    def atr(self):
        tr = np.abs(np.diff(self.prices[-(self.period + 1):]))
        atr_value = np.mean(tr)
        return Signal("ATR", round(atr_value, 4))

    def momentum(self):
        momentum_value = self.prices[-1] - self.prices[-self.period]
        return Signal("Momentum", round(momentum_value, 4))

    def roc(self):
        roc_value = ((self.prices[-1] - self.prices[-self.period]) / self.prices[-self.period]) * 100
        return Signal("ROC", round(roc_value, 2))

    def williams_r(self):
        low = np.min(self.prices[-self.period:])
        high = np.max(self.prices[-self.period:])
        close = self.prices[-1]
        wr = -100 * (high - close) / (high - low)
        return Signal("Williams_%R", round(wr, 2))

    def generate_signals(self):
        signals = [
            self.sma(),
            Signal("EMA", round(self.ema(), 4)),
            self.rsi(),
            *self.macd(),
            *self.bollinger_bands(),
            self.stochastic(),
            self.atr(),
            self.momentum(),
            self.roc(),
            self.williams_r()
        ]
        return signals
