import os
from google.cloud import language_v1
from dotenv import load_dotenv
import json

load_dotenv()

class PatternAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.client = language_v1.LanguageServiceClient.from_service_account_info({
            "type": "service_account",
            "project_id": "trado-project",
            "private_key_id": "",
            "private_key": "",
            "client_email": "",
            "client_id": "",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": ""
        })
        
    def analyze_pattern(self, pattern_data):
        """Analyze market patterns using Google Natural Language API"""
        # Convert pattern data to a structured format
        analysis_text = self._format_pattern_data(pattern_data)
        
        try:
            document = language_v1.Document(
                content=analysis_text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            # Analyze sentiment and entities
            sentiment = self.client.analyze_sentiment(request={'document': document}).document_sentiment
            entities = self.client.analyze_entities(request={'document': document}).entities
            
            # Generate analysis based on Google API results
            analysis = self._generate_trading_analysis(sentiment, entities, pattern_data)
            return analysis
            
        except Exception as e:
            return f"Error in pattern analysis: {str(e)}"
    
    def _format_pattern_data(self, pattern_data):
        """Format pattern data for analysis"""
        if isinstance(pattern_data, dict):
            df_dict = pattern_data
        else:
            df_dict = pattern_data.to_dict()
            
        # Create a descriptive text from the pattern data
        text = "Market analysis based on recent price action: "
        
        try:
            closes = list(df_dict['Close'].values())
            opens = list(df_dict['Open'].values())
            highs = list(df_dict['High'].values())
            lows = list(df_dict['Low'].values())
            
            # Calculate basic metrics
            trend = "upward" if closes[-1] > closes[0] else "downward"
            volatility = sum([h - l for h, l in zip(highs, lows)]) / len(highs)
            
            text += f"The market is showing a {trend} trend. "
            text += f"Price volatility is {volatility:.2f}. "
            text += f"Current price is {closes[-1]:.2f} with recent high of {max(highs):.2f} "
            text += f"and low of {min(lows):.2f}."
            
        except Exception as e:
            text += "Unable to process detailed metrics. Using basic pattern recognition."
            
        return text
    
    def _generate_trading_analysis(self, sentiment, entities, pattern_data):
        """Generate trading analysis based on Google API results"""
        analysis = {
            "pattern": "No clear pattern detected",
            "trend": "Neutral",
            "confidence": sentiment.score * 100,
            "suggestion": "Hold",
            "support_resistance": []
        }
        
        # Convert sentiment score to trading signals
        if sentiment.score > 0.2:
            analysis["trend"] = "Bullish"
            analysis["suggestion"] = "Consider buying with strict stop loss"
        elif sentiment.score < -0.2:
            analysis["trend"] = "Bearish"
            analysis["suggestion"] = "Consider selling with profit targets"
            
        # Pattern recognition based on price action
        if isinstance(pattern_data, dict):
            closes = list(pattern_data['Close'].values())
            if len(closes) >= 3:
                if closes[-1] > closes[-2] > closes[-3]:
                    analysis["pattern"] = "Ascending trend"
                elif closes[-1] < closes[-2] < closes[-3]:
                    analysis["pattern"] = "Descending trend"
                elif closes[-1] > closes[-2] and closes[-2] < closes[-3]:
                    analysis["pattern"] = "Potential reversal"
                    
        return json.dumps(analysis, indent=2)
            
    def analyze_pine_script(self, script):
        """Analyze Pine Script code using pattern matching"""
        common_errors = {
            "study": "strategy",
            "strategy.entry": "strategy.order",
            "security": "request.security",
        }
        
        analysis = {
            "errors": [],
            "suggestions": [],
            "corrected_code": script
        }
        
        # Basic error checking
        for old, new in common_errors.items():
            if old in script and old != new:
                analysis["errors"].append(f"Found deprecated function '{old}', should use '{new}'")
                analysis["corrected_code"] = analysis["corrected_code"].replace(old, new)
                
        # Check for basic syntax
        if "//" not in script:
            analysis["suggestions"].append("Add comments to explain your strategy")
            
        if "strategy.risk.max_drawdown" not in script:
            analysis["suggestions"].append("Consider adding drawdown protection")
            
        return json.dumps(analysis, indent=2)