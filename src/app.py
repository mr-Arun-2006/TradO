import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import datetime, timedelta

from market_data import MarketData
from trading_model import TradingModel
from pattern_analyzer import PatternAnalyzer

class TradoApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        try:
            self.market_data = MarketData()
        except Exception as e:
            print(f"Warning: Market data initialization failed: {e}")
            self.market_data = None
            
        self.trading_model = TradingModel()
        
        try:
            self.pattern_analyzer = PatternAnalyzer()
        except Exception as e:
            print(f"Warning: Pattern analyzer initialization failed: {e}")
            self.pattern_analyzer = None
        
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Trado - AI Trading Analysis"),
            
            # Symbol input
            html.Div([
                html.Label("Enter Stock/Index Symbol:"),
                dcc.Input(id='symbol-input', value='NIFTY50', type='text'),
                html.Button('Analyze', id='analyze-button'),
            ]),
            
            # Date range selector
            html.Div([
                html.Label("Select Date Range:"),
                dcc.DatePickerRange(
                    id='date-range',
                    start_date=(datetime.now() - timedelta(days=365)).date(),
                    end_date=datetime.now().date()
                ),
            ]),
            
            # Capital input
            html.Div([
                html.Label("Initial Capital:"),
                dcc.Input(id='capital-input', value='100000', type='number'),
            ]),
            
            # Charts and analysis
            html.Div([
                dcc.Graph(id='price-chart'),
                html.Div(id='model-results'),
                html.Div(id='pattern-analysis'),
            ]),
            
            # Pine Script section
            html.Div([
                html.Label("Pine Script Analysis:"),
                dcc.Textarea(
                    id='pine-script-input',
                    placeholder='Enter Pine Script code here...',
                    style={'width': '100%', 'height': 200},
                ),
                html.Button('Analyze Script', id='analyze-script-button'),
                html.Div(id='script-analysis-result'),
            ]),
        ])
        
    def setup_callbacks(self):
        @self.app.callback(
            [Output('price-chart', 'figure'),
             Output('model-results', 'children'),
             Output('pattern-analysis', 'children')],
            [Input('analyze-button', 'n_clicks')],
            [State('symbol-input', 'value'),
             State('date-range', 'start_date'),
             State('date-range', 'end_date'),
             State('capital-input', 'value')]
        )
        def update_analysis(n_clicks, symbol, start_date, end_date, capital):
            if n_clicks is None:
                return {}, "", ""
                
           
           # Get historical data
            try:
    # Get historical data
                if self.market_data is None:
                    return {}, "Error: Market data service not initialized", ""
                df = self.market_data.get_historical_data(symbol, start_date, end_date)
            except Exception as e:
    # Handle any errors that occur
                return {}, f"Error fetching data: {e}", ""
     
            # Train model and get predictions
            accuracy = self.trading_model.train(df)
            backtest_results = self.trading_model.backtest(df, float(capital))
            
            # Create price chart
            fig = go.Figure(data=[
                go.Candlestick(x=df.index,
                              open=df['Open'],
                              high=df['High'],
                              low=df['Low'],
                              close=df['Close'])
            ])
            
            # Get pattern analysis
            pattern_data = df.tail(10).to_dict()
            analysis = self.pattern_analyzer.analyze_pattern(pattern_data)
            
            return (
                fig,
                f"Model Accuracy: {accuracy:.2%}\n"
                f"Initial Capital: ₹{backtest_results['initial_capital']:,.2f}\n"
                f"Final Capital: ₹{backtest_results['final_capital']:,.2f}\n"
                f"Total Return: {backtest_results['total_return']:.2f}%",
                f"Pattern Analysis:\n{analysis}"
            )
            
        @self.app.callback(
            Output('script-analysis-result', 'children'),
            [Input('analyze-script-button', 'n_clicks')],
            [State('pine-script-input', 'value')]
        )
        def analyze_pine_script(n_clicks, script):
            if n_clicks is None or not script:
                return ""
            
            analysis = self.pattern_analyzer.analyze_pine_script(script)
            return analysis
            
    def run(self, debug=True):
        self.app.run_server(debug=debug)

if __name__ == '__main__':
    app = TradoApp()
    app.run()