"""
Data transformation module for the Stock Market Data Pipeline.
Handles data cleaning, validation, and standardization.
"""

from datetime import datetime
from utils import setup_logging, DataValidationError, validate_stock_data

logger = setup_logging(__name__)


def validate_date_format(date_string: str) -> bool:
    """
    Validate that date is in YYYY-MM-DD format.
    
    Args:
        date_string: Date string to validate
    
    Returns:
        True if date is valid, False otherwise
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def clean_symbol(symbol: str) -> str:
    """
    Clean and standardize stock symbol.
    
    Args:
        symbol: Stock symbol to clean
    
    Returns:
        Cleaned symbol (uppercase)
    """
    return symbol.upper().strip()


def clean_and_validate_record(record: dict) -> tuple[bool, dict, str]:
    """
    Clean and validate a single stock record.
    Performs data standardization and validation checks.
    
    Args:
        record: Dictionary containing stock data
    
    Returns:
        Tuple of (is_valid, cleaned_record, error_message)
    """
    try:
        # Clean symbol
        cleaned_record = record.copy()
        cleaned_record["symbol"] = clean_symbol(record.get("symbol", ""))
        
        # Validate and clean date
        date_str = record.get("date", "").strip()
        if not validate_date_format(date_str):
            return False, record, f"Invalid date format: {date_str}. Expected YYYY-MM-DD"
        cleaned_record["date"] = date_str
        
        # Convert and round prices to 2 decimals
        try:
            cleaned_record["open"] = round(float(record["open"]), 2)
            cleaned_record["high"] = round(float(record["high"]), 2)
            cleaned_record["low"] = round(float(record["low"]), 2)
            cleaned_record["close"] = round(float(record["close"]), 2)
            cleaned_record["volume"] = int(float(record.get("volume", 0)))
        except (ValueError, TypeError) as e:
            return False, record, f"Invalid numeric value: {e}"
        
        # Run comprehensive validation
        is_valid, error_msg = validate_stock_data(cleaned_record)
        if not is_valid:
            return False, record, error_msg
        
        return True, cleaned_record, ""
        
    except Exception as e:
        return False, record, f"Unexpected error cleaning record: {e}"


def transform_data(raw_records: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Transform raw data records: clean, validate, and prepare for loading.
    Separates valid and invalid records.
    
    Args:
        raw_records: List of raw data records from extraction
    
    Returns:
        Tuple of (valid_records, invalid_records_with_errors)
    """
    logger.info(f"Starting transformation of {len(raw_records)} records")
    
    valid_records = []
    invalid_records = []
    
    for i, record in enumerate(raw_records):
        is_valid, cleaned_record, error_msg = clean_and_validate_record(record)
        
        if is_valid:
            valid_records.append(cleaned_record)
        else:
            invalid_records.append({
                "index": i,
                "record": record,
                "error": error_msg
            })
            logger.debug(f"Record {i} validation failed: {error_msg}")
    
    logger.info(f"Transformation complete. Valid: {len(valid_records)}, Invalid: {len(invalid_records)}")
    
    # Log summary of invalid records
    if invalid_records:
        logger.warning(f"Found {len(invalid_records)} invalid records:")
        for invalid in invalid_records[:5]:  # Log first 5
            logger.warning(f"  Index {invalid['index']}: {invalid['error']}")
        if len(invalid_records) > 5:
            logger.warning(f"  ... and {len(invalid_records) - 5} more")
    
    return valid_records, invalid_records


def remove_duplicates(records: list[dict]) -> list[dict]:
    """
    Remove duplicate records based on symbol and date.
    Keeps the first occurrence of each symbol-date combination.
    
    Args:
        records: List of records
    
    Returns:
        List of records with duplicates removed
    """
    logger.info(f"Removing duplicates from {len(records)} records")
    
    seen = set()
    unique_records = []
    
    for record in records:
        key = (record["symbol"], record["date"])
        if key not in seen:
            seen.add(key)
            unique_records.append(record)
    
    removed = len(records) - len(unique_records)
    if removed > 0:
        logger.info(f"Removed {removed} duplicate records")
    
    return unique_records


def enrich_records(records: list[dict]) -> list[dict]:
    """
    Enrich records with computed fields (optional enhancement).
    Could add fields like daily_change, price_range, etc.
    
    Args:
        records: List of records to enrich
    
    Returns:
        Enriched records
    """
    logger.info(f"Enriching {len(records)} records")
    
    enriched = []
    for record in records:
        enriched_record = record.copy()
        
        # Calculate daily change
        open_price = record["open"]
        close_price = record["close"]
        daily_change = close_price - open_price
        daily_change_pct = (daily_change / open_price * 100) if open_price > 0 else 0
        
        # Add enriched fields
        enriched_record["daily_change"] = round(daily_change, 2)
        enriched_record["daily_change_pct"] = round(daily_change_pct, 2)
        enriched_record["price_range"] = round(record["high"] - record["low"], 2)
        
        enriched.append(enriched_record)
    
    return enriched


def transform_pipeline(raw_records: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Complete transformation pipeline combining all transformation steps.
    
    Args:
        raw_records: Raw extracted records
    
    Returns:
        Tuple of (transformed_records, invalid_records_with_errors)
    """
    logger.info("Starting complete transformation pipeline")
    
    # Step 1: Clean and validate
    valid_records, invalid_records = transform_data(raw_records)
    
    # Step 2: Remove duplicates
    unique_records = remove_duplicates(valid_records)
    
    # Step 3: Enrich with computed fields
    enriched_records = enrich_records(unique_records)
    
    logger.info(f"Transformation pipeline complete. Final records: {len(enriched_records)}")
    
    return enriched_records, invalid_records
