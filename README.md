# Stock Market Data Pipeline

An end-to-end ETL (Extract, Transform, Load) pipeline for collecting, cleaning, and storing stock market data.

## 🎯 Project Overview

This project demonstrates core data engineering skills:
- **Extract** data from multiple sources (APIs, CSV, web scraping)
- **Transform** and clean data
- **Load** into a relational database
- **Automate** the entire process

## 🛠 Tech Stack

- **Python 3.9+**
- **PostgreSQL** (or SQLite for local development)
- **Pandas** - Data manipulation
- **Requests** - API calls
- **SQLAlchemy** - Database ORM

## 📋 Features

- [ ] Extract stock data from multiple sources
- [ ] Data validation and error handling
- [ ] Automatic data transformation
- [ ] Database loading with upsert logic
- [ ] Logging and monitoring
- [ ] Automated daily refresh capability

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL (or SQLite)
- Git

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/stock-market-pipeline.git
cd stock-market-pipeline
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up database:
```bash
createdb stock_market  # PostgreSQL
# OR use SQLite (no setup needed)
```

5. Run the pipeline:
```bash
python main.py
```

## 📁 Project Structure

- `main.py` - Orchestrates the entire pipeline
- `extract.py` - Data extraction from sources
- `transform.py` - Data cleaning and transformation
- `load.py` - Database loading logic
- `requirements.txt` - Python dependencies
- `data/` - Raw data files
- `logs/` - Pipeline logs
- `notebooks/` - Exploratory analysis notebooks

## 📊 Data Sources

1. **API Source** - Real-time stock data
2. **CSV Source** - Historical data
3. **Web Source** - Scraped data (if applicable)

## 🔄 Pipeline Flow
Extract → Validate → Transform → Clean → Load → Verify

## 📝 Example Usage

```python
from main import run_pipeline

# Run full pipeline
run_pipeline()

# Or run individual components
from extract import extract_data
from transform import transform_data
from load import load_to_db

data = extract_data()
transformed = transform_data(data)
load_to_db(transformed)
```

## 🧪 Testing

```bash
pytest tests/
```

## 📈 Results

- Successfully processes X records per day
- Data validation accuracy: 99%+
- Pipeline execution time: < X minutes

## 🔍 Key Learnings

- ETL pipeline design and architecture
- Multi-source data integration
- Error handling and data validation
- Database design and optimization
- Automation and scheduling

## 📚 Resources

- [Pandas Documentation](https://pandas.pydata.org/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

[Your Name]
- Email: david.y.gaballa@gmail.com
- LinkedIn: www.linkedin.com/in/david-gaballa
- GitHub: [@DavidGaballa](https://github.com/david-gaballa)

---

**Last Updated:** June, 14, 2026
