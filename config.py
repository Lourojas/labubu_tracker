import os

# Alpha Vantage API configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

# Stock symbols for homepage display if not specified
DEFAULT_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

# Default time series function for getting stock data
DEFAULT_TIME_SERIES = "TIME_SERIES_DAILY"

# Chart configuration
CHART_PERIODS = {
    "1D": "TIME_SERIES_INTRADAY",
    "1W": "TIME_SERIES_DAILY",
    "1M": "TIME_SERIES_DAILY",
    "3M": "TIME_SERIES_DAILY",
    "1Y": "TIME_SERIES_DAILY",
    "5Y": "TIME_SERIES_WEEKLY"
}
