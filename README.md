# AliceBlue Trading Bot

An automated trading bot for AliceBlue, built with Python and Flask, that analyzes NSE stocks using TradingView technical indicators and executes trades based on predefined strategies.

## Features

- 🔐 Secure authentication with AliceBlue trading account
- 📊 Real-time market analysis using TradingView indicators
- 🤖 Automated trading based on technical analysis
- 💼 Portfolio and risk management
- 📱 Web interface for monitoring and control
- 📈 Analysis of top 25 NSE stocks
- 🔄 Automated order placement with risk calculation

## Prerequisites

- Python 3.6+
- AliceBlue trading account
- API credentials from AliceBlue

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aliceblue_bot.git
cd aliceblue_bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your AliceBlue credentials:
```env
API_SECRET=your_api_secret
APP_CODE=your_app_code
```

## Project Structure

```
├── app.py                 # Main Flask application
├── market_analyzer.py     # TradingView-based market analysis
├── auth.py               # AliceBlue authentication
├── strategy_engine.py    # Trading strategy implementation
├── risk.py              # Risk management calculations
├── order.py             # Order placement and management
├── account.py           # Account details handling
├── session_manager.py   # Session management
└── templates/           # Web interface templates
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5000`

3. Log in with your AliceBlue credentials

4. The bot will:
   - Analyze top 25 NSE stocks
   - Identify potential trading opportunities
   - Execute trades based on predefined strategies
   - Manage risk and position sizing

## Features in Detail

### Market Analysis
- Analyzes top 25 NSE stocks
- Uses TradingView technical indicators including:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Technical recommendations

### Trading Strategy
- Implements a combination of technical indicators
- Entry conditions based on:
  - RSI levels
  - MACD crossovers
  - Moving averages
- Risk management with position sizing

### Web Interface
- Real-time monitoring of trades
- Account information display
- Top stock picks visualization
- Order summary and execution status

## Security Features

- Secure session management
- Checksum-based API authentication
- Environment variable configuration
- Session validation for all trading operations

## Market Hours

The bot operates during NSE market hours:
- Monday to Friday
- 9:15 AM to 3:30 PM IST
- Excludes market holidays

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

This trading bot is for educational and research purposes only. Use it at your own risk. The creators are not responsible for any financial losses incurred through the use of this software.

## License

[MIT License](LICENSE)
