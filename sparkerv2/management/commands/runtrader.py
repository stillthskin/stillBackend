from django.core.management.base import BaseCommand
from sparkerv2.Trader import Trader
import os

class Command(BaseCommand):
    help = "Run the Binance trading bot"

    def handle(self, *args, **options):
        API_KEY = os.getenv("BINANCE_API_KEY")
        API_SECRET = os.getenv("BINANCE_API_SECRET")

        bot = Trader(API_KEY, API_SECRET, symbol="BTCUSDT", interval="15m", quantity=0.001)
        self.stdout.write(self.style.SUCCESS("🚀 Starting trading bot..."))
        bot.run(sleep_seconds=900)
