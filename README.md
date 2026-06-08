# Binance Futures Testnet Trading Bot

This is a Python CLI application that allows users to place Market, Limit, and Stop-Limit orders on the Binance Futures Testnet (USDT-M).

It is built with Python 3, `python-binance` for robust API interaction, and `Typer`/`Rich` for an enhanced command-line user experience.

## Features
- **Supported Orders:** MARKET, LIMIT, STOP_LIMIT (Bonus Feature)
- **Supported Sides:** BUY and SELL
- **Interactive CLI:** Prompts for missing fields, input validation, and summary confirmation before execution.
- **Robust Error Handling:** Catches API exceptions, network issues, and invalid input formats.
- **Detailed Logging:** Records API requests and responses to `trading_bot.log`.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Binance Futures Testnet account.
- Generated Testnet API keys (Key and Secret).

### 2. Installation
Clone or extract the repository, and navigate to the root directory.

Create a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Rename the `.env.example` file to `.env`:
```bash
# On Windows
copy .env.example .env
# On macOS/Linux
cp .env.example .env
```

Open the `.env` file and replace the placeholder values with your actual Binance Testnet API credentials:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

## How to Run Examples

You can run the bot and follow the interactive prompts:
```bash
python cli.py
```
Or you can provide the arguments directly to bypass some prompts.

### Place a MARKET Order
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Place a LIMIT Order
```bash
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.05 --price 3500
```

### Place a STOP_LIMIT Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type STOP_LIMIT --quantity 0.002 --price 65000 --stop-price 64000
```

### View Help
```bash
python cli.py --help
```

## Logs
All API interactions and internal operations are logged into the `trading_bot.log` file created in the root directory upon the first execution. Check this file for debugging or verification.

## Assumptions
- The application focuses specifically on **USDT-M Futures** (`https://testnet.binancefuture.com`).
- To place Limit and Stop-Limit orders, standard Binance rules require a `timeInForce` parameter. The bot hardcodes `GTC` (Good Till Cancelled) for simplicity.
- The `STOP_LIMIT` order is internally mapped to the `STOP` order type as per the Binance Futures API requirements for stop-limit orders.
