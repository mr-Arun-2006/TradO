import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import ta

class TradingModel:
    def __init__(self, initial_capital=100000):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.initial_capital = initial_capital
        
    def prepare_data(self, df):
        """Prepare data with technical indicators"""
        # Add technical indicators
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['MACD'] = ta.trend.MACD(df['Close']).macd()
        df['BB_upper'] = ta.volatility.BollingerBands(df['Close']).bollinger_hband()
        df['BB_lower'] = ta.volatility.BollingerBands(df['Close']).bollinger_lband()
        
        # Create target variable (1 for price increase, 0 for decrease)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        # Drop NaN values
        df = df.dropna()
        return df
        
    def train(self, df):
        """Train the model"""
        df = self.prepare_data(df)
        
        # Prepare features and target
        features = ['RSI', 'MACD', 'BB_upper', 'BB_lower', 'Open', 'High', 'Low', 'Close', 'Volume']
        X = df[features]
        y = df['Target']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model.fit(X_train, y_train)
        return self.model.score(X_test, y_test)
        
    def predict(self, data):
        """Make predictions"""
        df = self.prepare_data(data)
        features = ['RSI', 'MACD', 'BB_upper', 'BB_lower', 'Open', 'High', 'Low', 'Close', 'Volume']
        return self.model.predict(df[features].iloc[-1:])
        
    def backtest(self, df, capital=None):
        """Backtest the strategy"""
        if capital is None:
            capital = self.initial_capital
            
        df = self.prepare_data(df)
        features = ['RSI', 'MACD', 'BB_upper', 'BB_lower', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Make predictions for each day
        predictions = self.model.predict(df[features])
        
        # Calculate returns
        df['Position'] = predictions
        df['Returns'] = df['Close'].pct_change() * df['Position'].shift(1)
        
        # Calculate strategy performance
        cumulative_returns = (1 + df['Returns']).cumprod()
        final_capital = capital * cumulative_returns.iloc[-1]
        
        return {
            'initial_capital': capital,
            'final_capital': final_capital,
            'total_return': (final_capital - capital) / capital * 100,
            'daily_returns': df['Returns']
        }