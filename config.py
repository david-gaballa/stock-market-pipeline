"""
Configuration settings for the Stock Market Data Pipeline.
Centralized settings for easy management and adjustment.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Database configuration
DATABASE_PATH = PROJECT_ROOT / "data" / "stock_market.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
SAMPLE_DATA_DIR = PROJECT_ROOT / "sample_data"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
SAMPLE_DATA_DIR.mkdir(exist_ok=True)

# Logging configuration
LOG_FILE = LOGS_DIR / "pipeline.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Pipeline configuration
STOCKS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]  # Stocks to track

# Data source configurations
CSV_SOURCE_FILE = SAMPLE_DATA_DIR / "stock_data_sample.csv"
JSON_SOURCE_FILE = SAMPLE_DATA_DIR / "stock_data_sample.json"

# Validation rules
MIN_PRICE = 0.01
MAX_PRICE = 100000.00
MIN_VOLUME = 0
REQUIRED_COLUMNS = ["symbol", "date", "open", "high", "low", "close", "volume"]

# API configurations (if using external APIs in future)
TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
