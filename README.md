
# HCPCS Data Engineering Pipeline

## Project objective
Build a pipeline that extracts HCPCS data, preserves raw snapshots,
cleans records, loads PostgreSQL, and tracks description changes
using Slowly Changing Dimension Type 2 (SCD Type 2).

## Architecture
HCPCS website -> Python extraction -> Raw JSON -> pandas transformation
-> PostgreSQL SCD Type 2 -> Data quality checks -> Airflow

## Technologies
- Python
- Requests and BeautifulSoup
- pandas
- PostgreSQL
- Docker
- Apache Airflow
- pytest
- GitHub Actions

## Setup
1. Install Python, Git and Docker.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure `.env` using `.env.example`.
5. Start PostgreSQL using Docker Compose.
6. Execute the SQL schema script.
7. Run tests using `pytest -q`.
8. Run the pipeline using `python -m hcpcs_pipeline.pipeline`.

## Data quality
- Reject missing codes and descriptions.
- Deduplicate codes within each batch.
- Detect description changes using a hash.
- Validate current and historical versions.

## Limitations
Verify source terms, pagination, HTML structure, and completeness
before production use. This repository is a portfolio project,
not a production healthcare data service.
