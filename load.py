"""
Data loading module for the Stock Market Data Pipeline.
Handles loading transformed data into SQLite database.
"""

from database import insert_stock_data, create_database_schema, get_database_stats
from utils import setup_logging, DatabaseError, PipelineException

logger = setup_logging(__name__)


def prepare_for_loading(records: list[dict]) -> list[dict]:
    """
    Prepare records for database loading.
    Ensures all required fields are present and properly formatted.
    
    Args:
        records: Transformed records to prepare
    
    Returns:
        Prepared records ready for database insertion
    """
    logger.info(f"Preparing {len(records)} records for loading")
    
    prepared_records = []
    
    for record in records:
        # Only keep fields needed for database (exclude enrichment fields)
        prepared_record = {
            "symbol": record["symbol"],
            "date": record["date"],
            "open": record["open"],
            "high": record["high"],
            "low": record["low"],
            "close": record["close"],
            "volume": record["volume"]
        }
        prepared_records.append(prepared_record)
    
    logger.info(f"Prepared {len(prepared_records)} records for loading")
    return prepared_records


def load_to_database(records: list[dict]) -> dict:
    """
    Load prepared records into SQLite database.
    Handles database initialization and insertion with error handling.
    
    Args:
        records: Prepared records to load
    
    Returns:
        Dictionary with loading statistics
    
    Raises:
        DatabaseError: If loading fails
    """
    logger.info(f"Starting database load of {len(records)} records")
    
    if not records:
        logger.warning("No records to load")
        return {
            "status": "success",
            "inserted": 0,
            "updated": 0,
            "errors": 0
        }
    
    try:
        # Ensure database schema exists
        logger.info("Initializing database schema")
        create_database_schema()
        
        # Insert records
        logger.info("Inserting records into database")
        inserted, updated = insert_stock_data(records)
        
        logger.info(f"Database load complete. Inserted: {inserted}, Updated: {updated}")
        
        return {
            "status": "success",
            "inserted": inserted,
            "updated": updated,
            "errors": 0
        }
        
    except DatabaseError as e:
        logger.error(f"Database error during load: {e}")
        return {
            "status": "error",
            "inserted": 0,
            "updated": 0,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error during load: {e}")
        return {
            "status": "error",
            "inserted": 0,
            "updated": 0,
            "error": str(e)
        }


def load_pipeline(transformed_records: list[dict]) -> dict:
    """
    Complete loading pipeline.
    Prepares data and loads into database.
    
    Args:
        transformed_records: Records from transformation step
    
    Returns:
        Dictionary with pipeline execution statistics
    """
    logger.info("Starting load pipeline")
    
    # Prepare records
    prepared_records = prepare_for_loading(transformed_records)
    
    # Load to database
    load_result = load_to_database(prepared_records)
    
    # Get database statistics
    try:
        db_stats = get_database_stats()
        load_result["database_stats"] = db_stats
    except Exception as e:
        logger.warning(f"Could not retrieve database stats: {e}")
    
    logger.info(f"Load pipeline complete. Result: {load_result}")
    return load_result
