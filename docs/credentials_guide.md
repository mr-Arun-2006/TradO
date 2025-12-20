# Angel One Smart API Credentials Guide

## 1. Register/Login to Angel One Smart API
1. Go to https://smartapi.angelbroking.com/
2. Click "Login" or "Register" if you don't have an account
3. Use your Angel One trading account credentials

## 2. Get Your API Key
1. After logging in, go to the Smart API Dashboard
2. Look for "Generate API Key" or "API Keys" section
3. Click "Generate New API Key" if you don't have one
4. Note: You might need to verify your email/phone

## 3. Required Credentials

### API Key
- Found in: Smart API Dashboard > API Keys
- Format: Long alphanumeric string
- Example: "ab12cd34ef56gh78..." (keep this secret)

### Client ID
- This is your Angel One User ID
- Found in: Your Angel One trading account profile
- Format: Usually 6-8 characters
- Example: "AB1234"

### Password
- This is your Angel One trading password
- Use the same password you use for trading
- Make sure trading is enabled for your account

## 4. Security Best Practices
1. Never share your API key or credentials
2. Keep your .env file secure
3. Don't commit credentials to version control
4. Regularly rotate your API keys
5. Whitelist your IP address in the dashboard

## 5. Troubleshooting

If you get authentication errors:
1. Verify API key is active in dashboard
2. Check if your IP is whitelisted
3. Ensure trading password is correct
4. Make sure account has API trading enabled

Common Issues:
- "Invalid credentials": Check Client ID and password
- "Invalid API key": Regenerate API key
- "IP not allowed": Whitelist your IP address
- "Account not authorized": Enable API trading

For support:
1. Angel One Support: support@angelbroking.com
2. Smart API Documentation: https://smartapi.angelbroking.com/docs
3. Trading Support: 1800-209-8012