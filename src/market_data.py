import os
from smartapi import SmartConnect
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf

load_dotenv()

class MarketData:
    def __init__(self):
        self.api_key = os.getenv('ANGLE_ONE_API_KEY')
        self.client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
        self.password = os.getenv('ANGLE_ONE_PASSWORD')
        self.smart_api = SmartConnect(api_key=self.api_key)
        self.refresh_token = None
        self.access_token = None
        
    def connect(self):
        """Connect and generate session token"""
        try:
            data = self.smart_api.generateSession(self.client_id, self.password)
            if data['status']:
                self.refresh_token = data['data']['refreshToken']
                self.access_token = data['data']['jwt']
                # Save the tokens for reuse
                self.smart_api.set_token(self.access_token)
                return True
        except Exception as e:
            print(f"Error in connection: {str(e)}")
            return False
        
    def get_historical_data(self, symbol, start_date, end_date, interval='1d'):
        """Get historical data using yfinance for Indian stocks"""
        # Add .NS suffix for NSE stocks
        if not symbol.endswith('.NS'):
            symbol = f"{symbol}.NS"
        
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date, interval=interval)
        return df
        
    def get_live_data(self, symbol):
        """Get live market data from Angel One"""
        try:
            data = self.smart_api.ltpData("NSE", symbol, "EQ")
            return data
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return None