"""
Database setup and operations for Stock Market Data Pipeline.
Handles schema creation, connections, and data operations.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from config import DATABASE_PATH, DATABASE_URL
from utils import setup_logging, DatabaseError

logger = setup_logging(__name__)


def create_database_schema() -> None:
    """
    Create the stock_prices table if it doesn't exist.
    Handles the database schema with proper indexing and constraints.
    """
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        # Create stock_prices table with appropriate schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(symbol, date),
                CHECK(high >= low),
                CHECK(open > 0),
                CHECK(close > 0),
                CHECK(volume >= 0)
            )
        """)
        
        # Create index on symbol and date for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_symbol_date 
            ON stock_prices(symbol, date)
        """)
        
        # Create index on date for time-series queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date 
            ON stock_prices(date)
        """)
        
        connection.commit()
        logger.info(f"Database schema created/verified at {DATABASE_PATH}")
        
    except sqlite3.Error as e:
        logger.error(f"Database schema creation failed: {e}")
        raise DatabaseError(f"Failed to create database schema: {e}")
    finally:
        if connection:
            connection.close()


def insert_stock_data(records: list[dict]) -> tuple[int, int]:
    """
    Insert or update stock data records into the database.
    Uses REPLACE to handle duplicate entries (same symbol and date).
    
    Args:
        records: List of dictionaries containing stock data
    
    Returns:
        Tuple of (inserted_count, updated_count)
    
    Raises:
        DatabaseError: If insertion fails
    """
    if not records:
        logger.warning("No records to insert")
        return 0, 0
    
    connection = None
    inserted_count = 0
    updated_count = 0
    
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        for record in records:
            try:
                # Check if record exists
                cursor.execute(
                    "SELECT id FROM stock_prices WHERE symbol = ? AND date = ?",
                    (record["symbol"], record["date"])
                )
                exists = cursor.fetchone() is not None
                
                # Insert or update
                cursor.execute("""
                    INSERT OR REPLACE INTO stock_prices 
                    (symbol, date, open, high, low, close, volume, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    record["symbol"],
                    record["date"],
                    record["open"],
                    record["high"],
                    record["low"],
                    record["close"],
                    record["volume"],
                    datetime.now().isoformat()
                ))
                
                if exists:
                    updated_count += 1
                else:
                    inserted_count += 1
                    
            except sqlite3.IntegrityError as e:
                logger.warning(f"Skipping duplicate/invalid record {record}: {e}")
                continue
        
        connection.commit()
        logger.info(f"Inserted: {inserted_count}, Updated: {updated_count}")
        return inserted_count, updated_count
        
    except sqlite3.Error as e:
        logger.error(f"Database insertion failed: {e}")
        raise DatabaseError(f"Failed to insert stock data: {e}")
    finally:
        if connection:
            connection.close()


def get_latest_data(symbol: str, limit: int = 10) -> list[dict]:
    """
    Retrieve latest stock data for a given symbol.
    
    Args:
        symbol: Stock symbol
        limit: Number of records to retrieve
    
    Returns:
        List of dictionaries with stock data
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT symbol, date, open, high, low, close, volume 
            FROM stock_prices 
            WHERE symbol = ?
            ORDER BY date DESC
            LIMIT ?
        """, (symbol, limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve data: {e}")
        raise DatabaseError(f"Failed to retrieve stock data: {e}")
    finally:
        if connection:
            connection.close()


def get_database_stats() -> dict:
    """
    Get statistics about the database.
    
    Returns:
        Dictionary with database statistics
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        # Get total records
        cursor.execute("SELECT COUNT(*) as total FROM stock_prices")
        total = cursor.fetchone()[0]
        
        # Get unique symbols
        cursor.execute("SELECT COUNT(DISTINCT symbol) as symbols FROM stock_prices")
        symbols = cursor.fetchone()[0]
        
        # Get date range
        cursor.execute("SELECT MIN(date) as min_date, MAX(date) as max_date FROM stock_prices")
        min_date, max_date = cursor.fetchone()
        
        return {
            "total_records": total,
            "unique_symbols": symbols,
            "date_range": f"{min_date} to {max_date}" if min_date else "No data"
        }
        
    except sqlite3.Error as e:
        logger.error(f"Failed to get database stats: {e}")
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()
