"""
Utility functions for the Stock Market Data Pipeline.
Includes logging setup, error handling, and helper functions.
"""

import logging
import sys
from pathlib import Path
from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT


def setup_logging(name: str) -> logging.Logger:
    """
    Set up logging for the pipeline with both file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def validate_stock_data(row: dict) -> tuple[bool, str]:
    """
    Validate a single stock data row.
    
    Args:
        row: Dictionary containing stock data
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    from config import REQUIRED_COLUMNS, MIN_PRICE, MAX_PRICE, MIN_VOLUME
    
    # Check required columns exist
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in row]
    if missing_columns:
        return False, f"Missing required columns: {missing_columns}"
    
    # Validate symbol
    if not isinstance(row.get("symbol"), str) or len(row["symbol"]) == 0:
        return False, "Symbol must be a non-empty string"
    
    # Validate date
    if not isinstance(row.get("date"), str):
        return False, "Date must be a string"
    
    # Validate numeric fields
    try:
        open_price = float(row["open"])
        high_price = float(row["high"])
        low_price = float(row["low"])
        close_price = float(row["close"])
        volume = float(row["volume"])
    except (ValueError, TypeError) as e:
        return False, f"Price/volume values must be numeric: {e}"
    
    # Validate price ranges
    for price_field, price_value in [("open", open_price), ("high", high_price),
                                      ("low", low_price), ("close", close_price)]:
        if not (MIN_PRICE <= price_value <= MAX_PRICE):
            return False, f"{price_field} price {price_value} out of valid range"
    
    # Validate price logic (high >= low, etc)
    if not (high_price >= low_price):
        return False, "High price must be >= low price"
    
    if not (high_price >= open_price and high_price >= close_price):
        return False, "High price must be >= open and close prices"
    
    if not (low_price <= open_price and low_price <= close_price):
        return False, "Low price must be <= open and close prices"
    
    # Validate volume
    if volume < MIN_VOLUME:
        return False, f"Volume must be >= {MIN_VOLUME}"
    
    return True, ""


def ensure_directories() -> None:
    """Create necessary directories if they don't exist."""
    from config import DATA_DIR, LOGS_DIR, SAMPLE_DATA_DIR
    
    for directory in [DATA_DIR, LOGS_DIR, SAMPLE_DATA_DIR]:
        directory.mkdir(exist_ok=True)


class PipelineException(Exception):
    """Custom exception for pipeline errors."""
    pass


class DataValidationError(PipelineException):
    """Exception raised when data validation fails."""
    pass


class DataSourceError(PipelineException):
    """Exception raised when data source fails."""
    pass


class DatabaseError(PipelineException):
    """Exception raised when database operations fail."""
    pass
