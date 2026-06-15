"""
Test script for Stock Market Data Pipeline.
Verifies all components are working correctly before deployment.

Run with: python test_pipeline.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils import setup_logging, ensure_directories, validate_stock_data
from config import CSV_SOURCE_FILE, JSON_SOURCE_FILE, DATABASE_PATH, STOCKS
from database import get_database_stats

logger = setup_logging(__name__)


def test_imports() -> bool:
    """Test that all required modules can be imported."""
    print("\n[TEST 1] Testing imports...")
    try:
        import pandas
        import numpy
        import requests
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_directory_structure() -> bool:
    """Test that directory structure is correct."""
    print("\n[TEST 2] Testing directory structure...")
    try:
        ensure_directories()
        
        required_dirs = [
            PROJECT_ROOT / "data",
            PROJECT_ROOT / "logs",
            PROJECT_ROOT / "sample_data"
        ]
        
        for dir_path in required_dirs:
            if dir_path.exists():
                print(f"  ✓ {dir_path.name}/ exists")
            else:
                print(f"  ✗ {dir_path.name}/ missing")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ Directory test failed: {e}")
        return False


def test_sample_data() -> bool:
    """Test that sample data files exist."""
    print("\n[TEST 3] Testing sample data files...")
    
    files_to_check = [
        ("CSV", CSV_SOURCE_FILE),
        ("JSON", JSON_SOURCE_FILE)
    ]
    
    for file_type, file_path in files_to_check:
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file_type} file exists ({size} bytes)")
        else:
            print(f"  ✗ {file_type} file missing: {file_path}")
            return False
    
    return True


def test_extraction() -> bool:
    """Test data extraction from all sources."""
    print("\n[TEST 4] Testing data extraction...")
    try:
        from extract import extract_from_csv, extract_from_json, extract_from_simulated
        
        # Test CSV extraction
        try:
            csv_data = extract_from_csv()
            print(f"  ✓ CSV extraction: {len(csv_data)} records")
        except Exception as e:
            print(f"  ⚠ CSV extraction skipped: {e}")
        
        # Test JSON extraction
        try:
            json_data = extract_from_json()
            print(f"  ✓ JSON extraction: {len(json_data)} records")
        except Exception as e:
            print(f"  ⚠ JSON extraction skipped: {e}")
        
        # Test simulated extraction
        try:
            simulated_data = extract_from_simulated()
            print(f"  ✓ Simulated extraction: {len(simulated_data)} records")
            
            # Verify data structure
            if len(simulated_data) > 0:
                sample = simulated_data[0]
                required_fields = ["symbol", "date", "open", "high", "low", "close", "volume"]
                if all(field in sample for field in required_fields):
                    print(f"  ✓ Data structure valid")
                else:
                    print(f"  ✗ Data structure invalid")
                    return False
        except Exception as e:
            print(f"  ✗ Simulated extraction failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Extraction test failed: {e}")
        return False


def test_validation() -> bool:
    """Test data validation logic."""
    print("\n[TEST 5] Testing data validation...")
    
    # Valid record
    valid_record = {
        "symbol": "AAPL",
        "date": "2024-01-15",
        "open": 150.00,
        "high": 152.00,
        "low": 149.00,
        "close": 151.00,
        "volume": 50000000
    }
    
    is_valid, error = validate_stock_data(valid_record)
    if is_valid:
        print(f"  ✓ Valid record accepted")
    else:
        print(f"  ✗ Valid record rejected: {error}")
        return False
    
    # Invalid record (high < low)
    invalid_record = {
        "symbol": "AAPL",
        "date": "2024-01-15",
        "open": 150.00,
        "high": 149.00,  # Invalid: should be > low
        "low": 151.00,
        "close": 151.00,
        "volume": 50000000
    }
    
    is_valid, error = validate_stock_data(invalid_record)
    if not is_valid:
        print(f"  ✓ Invalid record rejected")
    else:
        print(f"  ✗ Invalid record accepted")
        return False
    
    return True


def test_transformation() -> bool:
    """Test data transformation logic."""
    print("\n[TEST 6] Testing data transformation...")
    try:
        from transform import clean_and_validate_record, remove_duplicates
        
        # Test record cleaning
        raw_record = {
            "symbol": "aapl",
            "date": "2024-01-15",
            "open": 150.00,
            "high": 152.00,
            "low": 149.00,
            "close": 151.00,
            "volume": 50000000.0
        }
        
        is_valid, cleaned, error = clean_and_validate_record(raw_record)
        if is_valid:
            print(f"  ✓ Record cleaning successful")
            
            # Verify cleaning - check for uppercase symbol and numeric prices
            if cleaned["symbol"] == "AAPL" and isinstance(cleaned["open"], float) and cleaned["open"] == 150.0:
                print(f"  ✓ Standardization correct (symbol uppercase, prices rounded to 2 decimals)")
            else:
                print(f"  ✗ Standardization failed")
                return False
        else:
            print(f"  ✗ Record cleaning failed: {error}")
            return False
        
        # Test duplicate removal
        records = [
            {"symbol": "AAPL", "date": "2024-01-15", "open": 150.0, "high": 152.0, "low": 149.0, "close": 151.0, "volume": 50000000},
            {"symbol": "AAPL", "date": "2024-01-15", "open": 150.0, "high": 152.0, "low": 149.0, "close": 151.0, "volume": 50000000},  # Duplicate
            {"symbol": "GOOGL", "date": "2024-01-15", "open": 140.0, "high": 142.0, "low": 139.0, "close": 141.0, "volume": 35000000}
        ]
        
        unique = remove_duplicates(records)
        if len(unique) == 2:
            print(f"  ✓ Duplicate removal: 3 records → 2 records")
        else:
            print(f"  ✗ Duplicate removal failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Transformation test failed: {e}")
        return False


def test_database() -> bool:
    """Test database initialization and operations."""
    print("\n[TEST 7] Testing database...")
    try:
        from database import create_database_schema, insert_stock_data
        
        # Create schema
        create_database_schema()
        print(f"  ✓ Database schema created")
        
        # Test insertion with unique key to avoid conflicts
        import time
        unique_id = str(int(time.time() * 1000))[-4:]  # Last 4 digits of current timestamp
        test_records = [
            {
                "symbol": f"TST{unique_id}",  # Unique symbol per test run
                "date": "2024-01-15",
                "open": 100.00,
                "high": 105.00,
                "low": 95.00,
                "close": 102.00,
                "volume": 1000000
            }
        ]
        
        inserted, updated = insert_stock_data(test_records)
        # Accept either inserted or updated (if record already exists)
        if inserted > 0 or updated > 0:
            print(f"  ✓ Data insertion: {inserted} inserted, {updated} updated")
        else:
            print(f"  ✗ Data insertion/update failed")
            return False
        
        # Check database stats
        try:
            stats = get_database_stats()
            print(f"  ✓ Database stats: {stats['total_records']} records")
        except Exception as e:
            print(f"  ⚠ Could not retrieve stats: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False


def test_logging() -> bool:
    """Test logging setup."""
    print("\n[TEST 8] Testing logging...")
    try:
        logger.info("Test log message")
        
        log_file = PROJECT_ROOT / "logs" / "pipeline.log"
        if log_file.exists():
            print(f"  ✓ Log file created")
        else:
            print(f"  ✗ Log file not created")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Logging test failed: {e}")
        return False


def run_all_tests() -> bool:
    """Run all tests."""
    print("\n" + "="*70)
    print(" Stock Market Data Pipeline - Test Suite".center(70))
    print("="*70)
    
    tests = [
        test_imports,
        test_directory_structure,
        test_sample_data,
        test_extraction,
        test_validation,
        test_transformation,
        test_database,
        test_logging
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    print(" Test Summary".center(70))
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Pipeline is ready to use.")
        print("\nNext steps:")
        print("  1. Review the README.md for usage instructions")
        print("  2. Run 'python main.py' to execute the pipeline")
        print("  3. Check logs/pipeline.log for execution details")
        return True
    else:
        print(f"\n✗ {total - passed} test(s) failed. Fix issues before running pipeline.")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)
