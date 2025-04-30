import os
import logging
import requests
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Alpha Vantage API base URL
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

@app.route("/")
def index():
    """Homepage displaying trending stocks."""
    try:
        # Get data for default stocks for homepage display
        stocks_data = []
        for symbol in config.DEFAULT_STOCKS:
            stock_data = get_stock_overview(symbol)
            if stock_data:
                stocks_data.append(stock_data)
            
        return render_template("index.html", stocks=stocks_data)
    except Exception as e:
        logger.error(f"Error rendering homepage: {str(e)}")
        return render_template("error.html", error="An error occurred while fetching stock data.")

@app.route("/search")
def search():
    """Search for stocks by keyword."""
    keyword = request.args.get("keyword", "")
    if not keyword:
        return redirect(url_for("index"))
    
    try:
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": keyword,
            "apikey": config.ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract search results from the response
        search_results = data.get("bestMatches", [])
        
        return render_template("search_results.html", results=search_results, keyword=keyword)
    except Exception as e:
        logger.error(f"Error searching for stocks: {str(e)}")
        return render_template("error.html", error="An error occurred while searching for stocks.")

@app.route("/stock/<symbol>")
def stock_detail(symbol):
    """Detailed view for a specific stock."""
    try:
        # Get the stock overview data
        stock_data = get_stock_overview(symbol)
        if not stock_data:
            return render_template("error.html", error=f"Stock data for {symbol} not found.")
        
        # Get historical data for charts
        time_period = request.args.get("period", "1M")
        historical_data = get_historical_data(symbol, time_period)
        
        return render_template(
            "stock_detail.html", 
            stock=stock_data, 
            historical_data=json.dumps(historical_data),
            periods=config.CHART_PERIODS.keys(),
            current_period=time_period
        )
    except Exception as e:
        logger.error(f"Error fetching stock detail for {symbol}: {str(e)}")
        return render_template("error.html", error=f"An error occurred while fetching data for {symbol}.")

@app.route("/api/stock/<symbol>/data")
def api_stock_data(symbol):
    """API endpoint to get stock data for AJAX requests."""
    try:
        time_period = request.args.get("period", "1M")
        historical_data = get_historical_data(symbol, time_period)
        return jsonify(historical_data)
    except Exception as e:
        logger.error(f"API error for {symbol}: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_stock_overview(symbol):
    """Get overview data for a stock."""
    try:
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": config.ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Check if we got a valid response
        if "Symbol" not in data:
            # Try to get basic quote data instead
            quote_params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": config.ALPHA_VANTAGE_API_KEY
            }
            quote_response = requests.get(ALPHA_VANTAGE_BASE_URL, params=quote_params)
            quote_response.raise_for_status()
            quote_data = quote_response.json()
            
            if "Global Quote" in quote_data and quote_data["Global Quote"]:
                return {
                    "Symbol": symbol,
                    "Name": symbol,  # Use symbol as name if not available
                    "Price": quote_data["Global Quote"].get("05. price", "N/A"),
                    "Change": quote_data["Global Quote"].get("09. change", "N/A"),
                    "ChangePercent": quote_data["Global Quote"].get("10. change percent", "N/A"),
                    "Description": "No detailed information available."
                }
            return None
        
        # Add additional price data from GLOBAL_QUOTE
        try:
            quote_params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": config.ALPHA_VANTAGE_API_KEY
            }
            quote_response = requests.get(ALPHA_VANTAGE_BASE_URL, params=quote_params)
            quote_response.raise_for_status()
            quote_data = quote_response.json()
            
            if "Global Quote" in quote_data and quote_data["Global Quote"]:
                data["Price"] = quote_data["Global Quote"].get("05. price", "N/A")
                data["Change"] = quote_data["Global Quote"].get("09. change", "N/A")
                data["ChangePercent"] = quote_data["Global Quote"].get("10. change percent", "N/A")
        except Exception as e:
            logger.warning(f"Could not fetch quote data for {symbol}: {str(e)}")
            data["Price"] = "N/A"
            data["Change"] = "N/A"
            data["ChangePercent"] = "N/A"
        
        return data
    except Exception as e:
        logger.error(f"Error fetching overview data for {symbol}: {str(e)}")
        return None

def get_historical_data(symbol, time_period):
    """Get historical stock data for charts."""
    try:
        # Determine the function and optional parameters based on time period
        function = config.CHART_PERIODS.get(time_period, config.DEFAULT_TIME_SERIES)
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": config.ALPHA_VANTAGE_API_KEY,
            "outputsize": "full"
        }
        
        # Add interval for intraday data
        if function == "TIME_SERIES_INTRADAY":
            params["interval"] = "5min"
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Parse the time series data based on the function
        if function == "TIME_SERIES_INTRADAY":
            time_series_key = f"Time Series (5min)"
        elif function == "TIME_SERIES_DAILY":
            time_series_key = "Time Series (Daily)"
        elif function == "TIME_SERIES_WEEKLY":
            time_series_key = "Weekly Time Series"
        elif function == "TIME_SERIES_MONTHLY":
            time_series_key = "Monthly Time Series"
        else:
            time_series_key = "Time Series (Daily)"  # Default
            
        time_series = data.get(time_series_key, {})
        
        # Format the data for Chart.js
        dates = []
        prices = []
        volumes = []
        
        # Limit the number of data points based on time period
        max_points = {
            "1D": 100,
            "1W": 7,
            "1M": 30,
            "3M": 90,
            "1Y": 365,
            "5Y": 260  # ~5 years of weekly data
        }.get(time_period, 30)
        
        # Sort dates in chronological order and limit to max_points
        sorted_dates = sorted(time_series.keys())
        if time_period in ["1D", "1W", "1M"]:
            # For shorter periods, show most recent data first
            sorted_dates = sorted_dates[-max_points:]
        else:
            # For longer periods, show older data first
            sorted_dates = sorted_dates[:max_points]
        
        for date in sorted_dates:
            daily_data = time_series[date]
            dates.append(date)
            prices.append(float(daily_data.get("4. close", 0)))
            volumes.append(float(daily_data.get("5. volume", 0)))
        
        return {
            "dates": dates,
            "prices": prices,
            "volumes": volumes
        }
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
        return {"dates": [], "prices": [], "volumes": []}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
