"""
Data extraction module for the Stock Market Data Pipeline.
Extracts stock data from multiple sources: CSV files, JSON files, and simulated data.
"""

import csv
import json
from datetime import datetime, timedelta
import random
from config import CSV_SOURCE_FILE, JSON_SOURCE_FILE, STOCKS
from utils import setup_logging, DataSourceError

logger = setup_logging(__name__)


def extract_from_csv() -> list[dict]:
    """
    Extract stock data from a CSV file.
    
    Expected CSV format: symbol, date, open, high, low, close, volume
    
    Returns:
        List of dictionaries containing stock data
    
    Raises:
        DataSourceError: If CSV file is not found or cannot be read
    """
    logger.info(f"Extracting data from CSV: {CSV_SOURCE_FILE}")
    
    if not CSV_SOURCE_FILE.exists():
        logger.error(f"CSV file not found: {CSV_SOURCE_FILE}")
        raise DataSourceError(f"CSV source file not found: {CSV_SOURCE_FILE}")
    
    try:
        records = []
        with open(CSV_SOURCE_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert string values to appropriate types
                record = {
                    "symbol": row["symbol"].upper(),
                    "date": row["date"],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": int(float(row["volume"]))
                }
                records.append(record)
        
        logger.info(f"Successfully extracted {len(records)} records from CSV")
        return records
        
    except FileNotFoundError as e:
        logger.error(f"CSV file not found: {e}")
        raise DataSourceError(f"CSV source file not found: {e}")
    except (ValueError, KeyError) as e:
        logger.error(f"CSV parsing error: {e}")
        raise DataSourceError(f"Failed to parse CSV file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading CSV: {e}")
        raise DataSourceError(f"Unexpected error reading CSV: {e}")


def extract_from_json() -> list[dict]:
    """
    Extract stock data from a JSON file.
    
    Expected JSON format: List of objects with keys: symbol, date, open, high, low, close, volume
    
    Returns:
        List of dictionaries containing stock data
    
    Raises:
        DataSourceError: If JSON file is not found or cannot be read
    """
    logger.info(f"Extracting data from JSON: {JSON_SOURCE_FILE}")
    
    if not JSON_SOURCE_FILE.exists():
        logger.error(f"JSON file not found: {JSON_SOURCE_FILE}")
        raise DataSourceError(f"JSON source file not found: {JSON_SOURCE_FILE}")
    
    try:
        with open(JSON_SOURCE_FILE, mode='r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Ensure data is a list
        if isinstance(data, dict):
            data = data.get("records", [])
        
        if not isinstance(data, list):
            raise DataSourceError("JSON data must be a list or dict with 'records' key")
        
        records = []
        for item in data:
            record = {
                "symbol": item.get("symbol", "").upper(),
                "date": item.get("date", ""),
                "open": float(item.get("open", 0)),
                "high": float(item.get("high", 0)),
                "low": float(item.get("low", 0)),
                "close": float(item.get("close", 0)),
                "volume": int(float(item.get("volume", 0)))
            }
            records.append(record)
        
        logger.info(f"Successfully extracted {len(records)} records from JSON")
        return records
        
    except FileNotFoundError as e:
        logger.error(f"JSON file not found: {e}")
        raise DataSourceError(f"JSON source file not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise DataSourceError(f"Failed to parse JSON file: {e}")
    except (ValueError, TypeError) as e:
        logger.error(f"JSON data format error: {e}")
        raise DataSourceError(f"JSON data format error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading JSON: {e}")
        raise DataSourceError(f"Unexpected error reading JSON: {e}")


def extract_from_simulated() -> list[dict]:
    """
    Extract simulated/mock stock data.
    Generates realistic stock price data for demonstration purposes.
    This simulates real-time or API-sourced data.
    
    Returns:
        List of dictionaries containing simulated stock data
    """
    logger.info("Extracting simulated stock data")
    
    records = []
    
    # Generate data for last 5 days
    for days_ago in range(5):
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        for symbol in STOCKS:
            # Generate realistic stock prices
            base_price = random.uniform(50, 500)
            
            open_price = base_price
            close_price = base_price * random.uniform(0.95, 1.05)
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.0)
            
            volume = random.randint(1000000, 50000000)
            
            record = {
                "symbol": symbol,
                "date": date,
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": volume
            }
            records.append(record)
    
    logger.info(f"Successfully generated {len(records)} simulated records")
    return records


def extract_all_sources() -> list[dict]:
    """
    Extract data from all available sources.
    Combines data from CSV, JSON, and simulated sources.
    
    Returns:
        List of all records from all sources
    """
    logger.info("Starting extraction from all sources")
    all_records = []
    source_results = {}
    
    # Extract from CSV
    try:
        csv_records = extract_from_csv()
        all_records.extend(csv_records)
        source_results["csv"] = {"status": "success", "count": len(csv_records)}
    except DataSourceError as e:
        logger.warning(f"CSV extraction skipped: {e}")
        source_results["csv"] = {"status": "skipped", "reason": str(e)}
    except Exception as e:
        logger.warning(f"CSV extraction failed: {e}")
        source_results["csv"] = {"status": "failed", "reason": str(e)}
    
    # Extract from JSON
    try:
        json_records = extract_from_json()
        all_records.extend(json_records)
        source_results["json"] = {"status": "success", "count": len(json_records)}
    except DataSourceError as e:
        logger.warning(f"JSON extraction skipped: {e}")
        source_results["json"] = {"status": "skipped", "reason": str(e)}
    except Exception as e:
        logger.warning(f"JSON extraction failed: {e}")
        source_results["json"] = {"status": "failed", "reason": str(e)}
    
    # Extract from simulated source (always available)
    try:
        simulated_records = extract_from_simulated()
        all_records.extend(simulated_records)
        source_results["simulated"] = {"status": "success", "count": len(simulated_records)}
    except Exception as e:
        logger.error(f"Simulated extraction failed: {e}")
        source_results["simulated"] = {"status": "failed", "reason": str(e)}
    
    logger.info(f"Extraction complete. Total records: {len(all_records)}")
    logger.info(f"Source results: {source_results}")
    
    return all_records
