"""
Main orchestrator for the Stock Market Data Pipeline.
Coordinates extraction, transformation, and loading of stock market data.

This module orchestrates the entire ETL pipeline, managing the flow from
data extraction through to database loading, with comprehensive error handling
and logging at each step.
"""

import sys
from datetime import datetime
from extract import extract_all_sources
from transform import transform_pipeline
from load import load_pipeline
from database import get_database_stats
from utils import setup_logging, ensure_directories, PipelineException

logger = setup_logging(__name__)


def print_banner() -> None:
    """Print pipeline startup banner."""
    print("\n" + "="*70)
    print(" Stock Market Data Pipeline - ETL Process".center(70))
    print("="*70 + "\n")


def print_statistics(result: dict) -> None:
    """
    Print pipeline execution statistics in a formatted way.
    
    Args:
        result: Dictionary containing pipeline execution results
    """
    print("\n" + "-"*70)
    print(" Pipeline Execution Summary".center(70))
    print("-"*70)
    
    if result.get("status") == "success":
        print(f"Status: ✓ SUCCESS")
        print(f"Timestamp: {result.get('timestamp')}")
        print(f"\nExtraction:")
        print(f"  Total records extracted: {result['extraction'].get('total', 0)}")
        
        print(f"\nTransformation:")
        print(f"  Valid records: {result['transformation'].get('valid', 0)}")
        print(f"  Invalid records: {result['transformation'].get('invalid', 0)}")
        
        print(f"\nLoading:")
        print(f"  Records inserted: {result['loading'].get('inserted', 0)}")
        print(f"  Records updated: {result['loading'].get('updated', 0)}")
        
        if "database_stats" in result:
            print(f"\nDatabase Statistics:")
            stats = result['database_stats']
            print(f"  Total records in database: {stats.get('total_records', 0)}")
            print(f"  Unique symbols: {stats.get('unique_symbols', 0)}")
            print(f"  Date range: {stats.get('date_range', 'No data')}")
        
        duration = result.get('duration', 'Unknown')
        print(f"\nTotal execution time: {duration}s")
        
    else:
        print(f"Status: ✗ FAILED")
        print(f"Error: {result.get('error')}")
    
    print("-"*70 + "\n")


def run_pipeline() -> dict:
    """
    Execute the complete stock market data pipeline.
    
    Orchestrates:
    1. Data extraction from multiple sources
    2. Data transformation and validation
    3. Data loading into SQLite database
    
    Returns:
        Dictionary with pipeline execution results and statistics
    
    Raises:
        PipelineException: If critical pipeline errors occur
    """
    
    start_time = datetime.now()
    logger.info("=" * 70)
    logger.info("STOCK MARKET DATA PIPELINE - STARTING")
    logger.info("=" * 70)
    
    result = {
        "status": "running",
        "timestamp": start_time.isoformat(),
        "extraction": {"total": 0},
        "transformation": {"valid": 0, "invalid": 0},
        "loading": {"inserted": 0, "updated": 0}
    }
    
    try:
        # Ensure directories exist
        logger.info("Setting up directories")
        ensure_directories()
        
        # STEP 1: EXTRACTION
        logger.info("\n" + "="*70)
        logger.info("STEP 1: DATA EXTRACTION")
        logger.info("="*70)
        
        try:
            extracted_records = extract_all_sources()
            logger.info(f"✓ Extraction successful: {len(extracted_records)} records")
            result["extraction"]["total"] = len(extracted_records)
            
            if len(extracted_records) == 0:
                logger.warning("Warning: No records extracted. Check data sources.")
                
        except PipelineException as e:
            logger.error(f"✗ Extraction failed: {e}")
            result["status"] = "error"
            result["error"] = f"Extraction failed: {e}"
            return result
        except Exception as e:
            logger.error(f"✗ Unexpected error during extraction: {e}")
            result["status"] = "error"
            result["error"] = f"Unexpected extraction error: {e}"
            return result
        
        # STEP 2: TRANSFORMATION
        logger.info("\n" + "="*70)
        logger.info("STEP 2: DATA TRANSFORMATION")
        logger.info("="*70)
        
        try:
            transformed_records, invalid_records = transform_pipeline(extracted_records)
            logger.info(f"✓ Transformation successful:")
            logger.info(f"  Valid records: {len(transformed_records)}")
            logger.info(f"  Invalid records: {len(invalid_records)}")
            
            result["transformation"]["valid"] = len(transformed_records)
            result["transformation"]["invalid"] = len(invalid_records)
            
            if len(transformed_records) == 0:
                logger.error("✗ No valid records after transformation. Cannot proceed.")
                result["status"] = "error"
                result["error"] = "No valid records after transformation"
                return result
                
        except PipelineException as e:
            logger.error(f"✗ Transformation failed: {e}")
            result["status"] = "error"
            result["error"] = f"Transformation failed: {e}"
            return result
        except Exception as e:
            logger.error(f"✗ Unexpected error during transformation: {e}")
            result["status"] = "error"
            result["error"] = f"Unexpected transformation error: {e}"
            return result
        
        # STEP 3: LOADING
        logger.info("\n" + "="*70)
        logger.info("STEP 3: DATA LOADING")
        logger.info("="*70)
        
        try:
            load_result = load_pipeline(transformed_records)
            
            if load_result.get("status") == "success":
                logger.info(f"✓ Loading successful:")
                logger.info(f"  Records inserted: {load_result['inserted']}")
                logger.info(f"  Records updated: {load_result['updated']}")
                
                result["loading"]["inserted"] = load_result["inserted"]
                result["loading"]["updated"] = load_result["updated"]
                
                if "database_stats" in load_result:
                    result["database_stats"] = load_result["database_stats"]
                    
            else:
                logger.error(f"✗ Loading failed: {load_result.get('error')}")
                result["status"] = "error"
                result["error"] = f"Loading failed: {load_result.get('error')}"
                return result
                
        except PipelineException as e:
            logger.error(f"✗ Loading failed: {e}")
            result["status"] = "error"
            result["error"] = f"Loading failed: {e}"
            return result
        except Exception as e:
            logger.error(f"✗ Unexpected error during loading: {e}")
            result["status"] = "error"
            result["error"] = f"Unexpected loading error: {e}"
            return result
        
        # PIPELINE COMPLETE
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        result["status"] = "success"
        result["duration"] = round(duration, 2)
        
        logger.info("\n" + "="*70)
        logger.info("PIPELINE EXECUTION COMPLETE - SUCCESS")
        logger.info("="*70)
        
        return result
        
    except Exception as e:
        logger.error(f"✗ Unexpected error in pipeline: {e}", exc_info=True)
        result["status"] = "error"
        result["error"] = f"Unexpected pipeline error: {e}"
        return result


def main() -> int:
    """
    Main entry point for the pipeline.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        print_banner()
        
        # Run the pipeline
        result = run_pipeline()
        
        # Print results
        print_statistics(result)
        
        # Return appropriate exit code
        if result.get("status") == "success":
            print("✓ Pipeline completed successfully!")
            return 0
        else:
            print("✗ Pipeline failed. Check logs for details.")
            return 1
            
    except KeyboardInterrupt:
        logger.error("Pipeline interrupted by user")
        print("\n\n✗ Pipeline interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n\n✗ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
