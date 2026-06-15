# Stock Market Data Pipeline

An **end-to-end ETL (Extract, Transform, Load) pipeline** for collecting, validating, cleaning, and storing stock market data in a relational database. This project demonstrates core data engineering principles and best practices.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Database](https://img.shields.io/badge/database-SQLite-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📊 Project Overview

This pipeline automates the collection and management of stock market data from multiple sources. It demonstrates:

- **Multi-source data integration** (CSV, JSON, API simulation)
- **Robust data validation** with comprehensive error handling
- **Data transformation and cleaning** with detailed logging
- **Database design** with proper schema and indexing
- **Production-ready code** with documentation and testing capability

### Key Features

✅ Extract from multiple sources simultaneously
✅ Validate and clean data with detailed error reporting
✅ Transform and enrich data with computed fields
✅ Load into SQLite with duplicate handling
✅ Comprehensive logging and error tracking
✅ Database statistics and monitoring
✅ Modular, maintainable architecture

---

## 🏗️ Architecture

```
Raw Data Sources
    ├── CSV Files
    ├── JSON Files
    └── API/Simulated Data
         ↓
    ┌─────────────────┐
    │   EXTRACT       │  (extract.py)
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │   TRANSFORM     │  (transform.py)
    │  • Clean        │
    │  • Validate     │
    │  • Enrich       │
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │   LOAD          │  (load.py)
    │  • Insert       │
    │  • Update       │
    │  • Verify       │
    └────────┬────────┘
             ↓
       SQLite Database
```

---

## 📁 Project Structure

```
stock-market-pipeline/
├── main.py                          # Pipeline orchestrator
├── extract.py                       # Data extraction module
├── transform.py                     # Data cleaning & validation
├── load.py                          # Database loading
├── database.py                      # DB schema & operations
├── config.py                        # Configuration settings
├── utils.py                         # Helper functions & logging
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── data/                            # Database storage
│   └── stock_market.db             # SQLite database
├── logs/                            # Pipeline execution logs
│   └── pipeline.log                # Detailed execution log
└── sample_data/                     # Sample data sources
    ├── stock_data_sample.csv       # CSV sample data
    └── stock_data_sample.json      # JSON sample data
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Database | SQLite 3 |
| Data Processing | Pandas, NumPy |
| HTTP Requests | Requests |
| Data Format | CSV, JSON |
| Logging | Python logging |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- ~50MB disk space

### Installation Steps

1. **Clone the repository** (or download the project files):
```bash
cd stock-market-pipeline
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Verify installation**:
```bash
python -c "import pandas; print('✓ Setup successful!')"
```

---

## 🚀 Running the Pipeline

### Quick Start

```bash
python main.py
```

This will:
1. Extract data from all sources (CSV, JSON, simulated)
2. Validate and clean the data
3. Load into SQLite database
4. Display execution summary

### Example Output

```
======================================================================
 Stock Market Data Pipeline - ETL Process
======================================================================

======================================================================
STOCK MARKET DATA PIPELINE - STARTING
======================================================================

======================================================================
STEP 1: DATA EXTRACTION
======================================================================
[INFO] Extracting data from CSV: sample_data/stock_data_sample.csv
[INFO] Successfully extracted 10 records from CSV
[INFO] Extracting data from JSON: sample_data/stock_data_sample.json
[INFO] Successfully extracted 5 records from JSON
[INFO] Extracting simulated stock data
[INFO] Successfully generated 25 simulated records

... (transformation and loading steps) ...

======================================================================
PIPELINE EXECUTION COMPLETE - SUCCESS
======================================================================

----------------------------------------------------------------------
 Pipeline Execution Summary
----------------------------------------------------------------------
Status: ✓ SUCCESS
Timestamp: 2024-01-18T10:45:32.123456

Extraction:
  Total records extracted: 40

Transformation:
  Valid records: 40
  Invalid records: 0

Loading:
  Records inserted: 40
  Records updated: 0

Database Statistics:
  Total records in database: 40
  Unique symbols: 5
  Date range: 2024-01-15 to 2024-01-17

Total execution time: 2.34s
----------------------------------------------------------------------
```

---

## 📋 Detailed Module Documentation

### 1. **main.py** - Pipeline Orchestrator

The main entry point that coordinates the entire ETL process.

**Key Functions:**
- `run_pipeline()` - Executes extract → transform → load sequence
- `print_statistics()` - Displays execution results
- `main()` - Entry point with error handling

**Usage:**
```bash
python main.py
```

### 2. **extract.py** - Data Extraction

Extracts data from multiple sources with error handling.

**Data Sources:**
- **CSV Files**: `sample_data/stock_data_sample.csv`
- **JSON Files**: `sample_data/stock_data_sample.json`
- **Simulated Data**: Generated realistic test data

**Key Functions:**
- `extract_from_csv()` - Extract from CSV source
- `extract_from_json()` - Extract from JSON source
- `extract_from_simulated()` - Generate simulated data
- `extract_all_sources()` - Combine all sources

**Expected Data Format:**
```
symbol: Stock ticker (e.g., "AAPL")
date: Date in YYYY-MM-DD format
open: Opening price (float)
high: High price (float)
low: Low price (float)
close: Closing price (float)
volume: Trading volume (integer)
```

### 3. **transform.py** - Data Transformation

Validates, cleans, and enriches data.

**Transformations:**
1. **Cleaning**: Standardizes symbols, formats dates
2. **Validation**: Checks data types, ranges, logical consistency
3. **Deduplication**: Removes duplicate symbol-date combinations
4. **Enrichment**: Adds computed fields (daily_change, price_range)

**Key Functions:**
- `clean_and_validate_record()` - Validate and clean single record
- `transform_data()` - Transform batch of records
- `remove_duplicates()` - Eliminate duplicate entries
- `enrich_records()` - Add computed fields
- `transform_pipeline()` - Complete transformation workflow

**Validation Rules:**
- Symbol: Non-empty uppercase string
- Date: Valid YYYY-MM-DD format
- Prices: Between $0.01 and $100,000
- High ≥ Low, High ≥ Open/Close, Low ≤ Open/Close
- Volume: Non-negative integer

### 4. **load.py** - Database Loading

Loads transformed data into SQLite database.

**Features:**
- Creates database schema if needed
- Handles duplicate records (INSERT OR REPLACE)
- Tracks insert vs. update operations
- Provides database statistics

**Key Functions:**
- `prepare_for_loading()` - Format data for database
- `load_to_database()` - Insert/update records
- `load_pipeline()` - Complete loading workflow

### 5. **database.py** - Database Operations

Manages SQLite database schema and operations.

**Database Schema:**
```sql
CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(symbol, date),
    CHECK(high >= low),
    ...
)
```

**Indexes:**
- `idx_symbol_date`: Fast queries by symbol and date
- `idx_date`: Fast time-series queries

**Key Functions:**
- `create_database_schema()` - Initialize database
- `insert_stock_data()` - Add/update records
- `get_latest_data()` - Retrieve recent records
- `get_database_stats()` - Database statistics

### 6. **config.py** - Configuration

Centralized configuration for the pipeline.

**Settings:**
- Database path and connection
- Directory paths (data, logs, sample_data)
- Logging configuration
- Stock symbols to track
- Data source file paths
- Validation rules and ranges

**Modify for Production:**
```python
# Change stock symbols
STOCKS = ["AAPL", "GOOGL", "MSFT"]

# Change database location
DATABASE_PATH = Path("/data/production/stock_market.db")

# Adjust validation ranges
MIN_PRICE = 0.01
MAX_PRICE = 100000.00
```

### 7. **utils.py** - Utility Functions

Helper functions for logging, validation, and error handling.

**Key Functions:**
- `setup_logging()` - Configure file and console logging
- `validate_stock_data()` - Validate record fields
- `ensure_directories()` - Create necessary directories

**Custom Exceptions:**
- `PipelineException` - Base exception
- `DataValidationError` - Validation failures
- `DataSourceError` - Source access failures
- `DatabaseError` - Database operation failures

---

## 📊 Data Validation & Error Handling

### Validation Process

1. **Completeness**: All required fields present
2. **Type Checking**: Correct data types
3. **Range Validation**: Values within acceptable ranges
4. **Logical Consistency**: Price relationships valid
5. **Format Validation**: Dates in correct format

### Error Handling

- **Extraction Errors**: Skips unavailable source, logs details
- **Validation Errors**: Records logged with specific error messages
- **Database Errors**: Detailed error tracking and rollback
- **Unexpected Errors**: Full stack traces in logs

### Example Invalid Records

Invalid records are logged with explanations:
```
[WARNING] Record 5 validation failed: High price must be >= low price
[WARNING] Record 12 validation failed: Invalid date format: 01/15/2024. Expected YYYY-MM-DD
[WARNING] Record 18 validation failed: Price values must be numeric: could not convert string to float
```

---

## 📈 Query Examples

After running the pipeline, query your data:

### Python

```python
from database import get_latest_data, get_database_stats

# Get latest 10 AAPL records
data = get_latest_data("AAPL", limit=10)
for record in data:
    print(f"{record['date']}: ${record['close']}")

# Get database statistics
stats = get_database_stats()
print(f"Total records: {stats['total_records']}")
print(f"Symbols tracked: {stats['unique_symbols']}")
```

### SQLite Command Line

```bash
sqlite3 data/stock_market.db

# View all records for AAPL
SELECT * FROM stock_prices WHERE symbol = 'AAPL';

# Get price range for each symbol
SELECT symbol, MIN(close) as min_price, MAX(close) as max_price
FROM stock_prices
GROUP BY symbol;

# Calculate daily changes
SELECT symbol, date, 
  ROUND((close - open) / open * 100, 2) as pct_change
FROM stock_prices
WHERE symbol = 'AAPL'
ORDER BY date DESC;
```

---

## 🧪 Testing

### Manual Testing

1. **Verify Sample Data**:
```bash
# Check CSV file
head sample_data/stock_data_sample.csv

# Check JSON file
python -m json.tool sample_data/stock_data_sample.json
```

2. **Run Pipeline**:
```bash
python main.py
```

3. **Verify Database**:
```bash
sqlite3 data/stock_market.db "SELECT COUNT(*) FROM stock_prices;"
```

4. **Check Logs**:
```bash
tail -f logs/pipeline.log
```

### Adding Test Data

Create `sample_data/test_invalid.csv` to test validation:
```csv
symbol,date,open,high,low,close,volume
AAPL,2024-01-18,150.00,149.00,151.00,150.50,50000000
MSFT,invalid-date,380.00,390.00,370.00,385.00,30000000
```

---

## 📚 Production Deployment

### For Real-Time Data

Replace simulated data source in `extract.py`:

```python
def extract_from_api() -> list[dict]:
    """Extract from real stock API (Alpha Vantage, IEX, etc.)"""
    # Implementation here
    pass
```

### For Scheduled Runs

Create a cron job (Linux/Mac):
```bash
# Run pipeline daily at 4 PM
0 16 * * * cd /path/to/pipeline && python main.py >> logs/cron.log 2>&1
```

Windows Task Scheduler:
```
Program: python
Arguments: C:\path\to\main.py
Schedule: Daily at 4 PM
```

### Database Backup

```bash
# SQLite backup
cp data/stock_market.db data/stock_market.backup.db

# Or use SQLite commands
sqlite3 data/stock_market.db ".backup data/stock_market.backup.db"
```

---

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"

**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### "No records extracted"

**Solution**: Check that sample data files exist
```bash
ls -la sample_data/
```

### "Database is locked"

**Solution**: Only one process can write at a time. Close other connections.

### "Invalid data format" errors

**Solution**: Check CSV/JSON format matches expected schema. See Data Format section.

### Large execution time

**Solution**: Check logs for timeout errors. Increase timeout in `config.py`:
```python
TIMEOUT = 60  # seconds
```

---

## 📈 Key Learning Outcomes

This project demonstrates understanding of:

1. **ETL Architecture**
   - Separation of concerns (Extract/Transform/Load)
   - Error handling at each stage
   - Data validation strategies

2. **Data Engineering**
   - Multi-source data integration
   - Data cleaning and standardization
   - Schema design and indexing
   - Duplicate handling

3. **Software Engineering**
   - Modular code design
   - Comprehensive logging
   - Error handling and recovery
   - Configuration management

4. **Database Design**
   - Relational schema design
   - Constraints and validation
   - Indexing for performance
   - UPSERT operations

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👤 Author

**David Gaballa**
- Email: david.y.gaballa@gmail.com
- LinkedIn: www.linkedin.com/in/david-gaballa
- GitHub: [@DavidGaballa](https://github.com/david-gaballa)

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Create a branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📞 Support

For questions or issues:
1. Check the Troubleshooting section
2. Review logs in `logs/pipeline.log`
3. Verify data format matches schema
4. Check configuration in `config.py`

---

## 🎯 Next Steps

- Add real API data source (Alpha Vantage, IEX Cloud)
- Implement automated scheduling
- Add data visualization dashboard
- Create unit tests
- Deploy to cloud (AWS/GCP)

---

**Last Updated**: June 2026
**Status**: ✓ Production Ready
