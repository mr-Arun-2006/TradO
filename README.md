# Trado - AI Trading Analysis Platform

Trado is an advanced AI-powered trading analysis platform for Indian markets that combines historical data analysis, real-time market data, and AI-driven pattern recognition to help traders make informed decisions.

## Features

- Historical data analysis for Indian stocks and indices
- Real-time market data integration with Angel One Smart API
- AI-powered trading model with backtesting capabilities
- Technical indicator analysis
- Pattern recognition using ChatGPT
- Pine Script analysis and error correction
- Interactive web interface with charts and analytics

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
ANGLE_ONE_API_KEY=your_api_key_here
ANGLE_ONE_CLIENT_ID=your_client_id
ANGLE_ONE_PASSWORD=your_password
ANGLE_ONE_TOKEN=your_token
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Run the application:
```bash
python src/app.py
```

2. Open your web browser and navigate to `http://localhost:8050`

3. Enter a stock symbol or index (e.g., "NIFTY50", "RELIANCE.NS")

4. Select the date range for analysis

5. Enter your initial capital for backtesting

6. Click "Analyze" to get:
   - Price charts with technical indicators
   - AI model predictions and backtesting results
   - Pattern analysis using ChatGPT
   - Trading suggestions

7. Use the Pine Script analysis section to check and improve your trading strategies

## Components

- `market_data.py`: Handles data retrieval from Angel One API and Yahoo Finance
- `trading_model.py`: Implements the AI trading model and backtesting functionality
- `pattern_analyzer.py`: Integrates with ChatGPT for pattern analysis
- `app.py`: Main application with Dash web interface

## Notes

- Make sure to replace the API keys in the `.env` file with your own
- The model uses Random Forest for predictions, but can be extended with other algorithms
- Pine Script analysis requires an OpenAI API key
- Real-time data requires an Angel One account and API access