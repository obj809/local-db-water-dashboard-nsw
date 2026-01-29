# Local Database Water Dashboard NSW

## Project Overview
A local MySQL-based system for tracking and analyzing dam data across NSW, Australia. Built with Python, MySQL, Pandas, and OpenPyXL.

## Table of Contents
- [Goals & MVP](#goals--mvp)
- [Tech Stack](#tech-stack)
- [How To Use](#how-to-use)
- [Design Goals](#design-goals)
- [Project Features](#project-features)
- [Additions & Improvements](#additions--improvements)
- [Learning Highlights](#learning-highlights)
- [Known Issues](#known-issues)
- [Challenges](#challenges)

## Goals & MVP
Create a centralized system that stores dam metadata, tracks water storage levels, archives historical data, and generates analytical reports with rolling averages (12-month, 5-year, 20-year) for 34 NSW dams.

## Tech Stack
- Python 3
- MySQL 8.0+
- Pandas
- OpenPyXL
- python-dotenv

## How To Use
1. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with MySQL credentials (LOCAL_DB_HOST, LOCAL_DB_PORT, LOCAL_DB_NAME, LOCAL_DB_USER, LOCAL_DB_PASSWORD)
4. Run database setup: `python3 scripts/local_db_create_db.py && python3 scripts/local_db_create_schema.py && python3 scripts/local_db_seed_data.py`
5. Export to Excel: `python scripts/local_export_mysql_to_excel.py`

## Design Goals
- **Data Integrity**: Foreign keys with cascading relationships
- **Idempotency**: Upsert operations for safe re-runs
- **Security**: Parameterized queries to prevent SQL injection
- **Modularity**: Separate seeding scripts with dependency-ordered execution

## Project Features
- [x] 34 NSW dams with metadata (capacity, coordinates, identifiers)
- [x] Dam grouping system (Sydney, popular, large, small, greatest released)
- [x] 24-month historical snapshots with rolling average analysis
- [x] Excel export with customizable table filtering

## Learning Highlights
- Normalized database schema design with foreign key relationships
- Orchestrated data pipelines with dependency ordering
- Upsert patterns and composite keys in SQL

## Known Issues
- Local MySQL only; no cloud deployment configuration
- Synthetic data; does not reflect actual NSW dam levels
- Manual refresh required; no automated scheduling

## Challenges
- Establishing correct seeding order for foreign key constraints
- Designing composite primary keys for analysis tables
- Generating realistic synthetic historical data patterns

```SQL
CREATE TABLE dams (
    dam_id VARCHAR(20) PRIMARY KEY,
    dam_name VARCHAR(255) NOT NULL,
    full_volume INT,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6)
);

CREATE TABLE latest_data (
    dam_id VARCHAR(20) PRIMARY KEY,
    dam_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    storage_volume DECIMAL(10, 3),
    percentage_full DECIMAL(6, 2),
    storage_inflow DECIMAL(10, 3),
    storage_release DECIMAL(10, 3),
    FOREIGN KEY (dam_id) REFERENCES dams(dam_id)
);

CREATE TABLE dam_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    dam_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    storage_volume DECIMAL(10, 3),
    percentage_full DECIMAL(6, 2),
    storage_inflow DECIMAL(10, 3),
    storage_release DECIMAL(10, 3),
    FOREIGN KEY (dam_id) REFERENCES dams(dam_id)
);

CREATE TABLE specific_dam_analysis (
    dam_id VARCHAR(20),
    analysis_date DATE,
    avg_storage_volume_12_months DECIMAL(10, 3),
    avg_storage_volume_5_years DECIMAL(10, 3),
    avg_storage_volume_20_years DECIMAL(10, 3),
    avg_percentage_full_12_months DECIMAL(6, 2),
    avg_percentage_full_5_years DECIMAL(6, 2),
    avg_percentage_full_20_years DECIMAL(6, 2),
    avg_storage_inflow_12_months DECIMAL(10, 3),
    avg_storage_inflow_5_years DECIMAL(10, 3),
    avg_storage_inflow_20_years DECIMAL(10, 3),
    avg_storage_release_12_months DECIMAL(10, 3),
    avg_storage_release_5_years DECIMAL(10, 3),
    avg_storage_release_20_years DECIMAL(10, 3),
    PRIMARY KEY (dam_id, analysis_date),
    FOREIGN KEY (dam_id) REFERENCES dams(dam_id)
);

CREATE TABLE overall_dam_analysis (
    analysis_date DATE PRIMARY KEY,
    avg_storage_volume_12_months DECIMAL(10, 3),
    avg_storage_volume_5_years DECIMAL(10, 3),
    avg_storage_volume_20_years DECIMAL(10, 3),
    avg_percentage_full_12_months DECIMAL(6, 2),
    avg_percentage_full_5_years DECIMAL(6, 2),
    avg_percentage_full_20_years DECIMAL(6, 2),
    avg_storage_inflow_12_months DECIMAL(10, 3),
    avg_storage_inflow_5_years DECIMAL(10, 3),
    avg_storage_inflow_20_years DECIMAL(10, 3),
    avg_storage_release_12_months DECIMAL(10, 3),
    avg_storage_release_5_years DECIMAL(10, 3),
    avg_storage_release_20_years DECIMAL(10, 3)
);

CREATE TABLE dam_groups (
    group_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE dam_group_members (
    group_name VARCHAR(255) NOT NULL,
    dam_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (group_name, dam_id),
    FOREIGN KEY (group_name) REFERENCES dam_groups(group_name),
    FOREIGN KEY (dam_id) REFERENCES dams(dam_id)
);
```

## Contact Me
- Visit my [LinkedIn](https://www.linkedin.com/in/obj809/) for more details.
- Check out my [GitHub](https://github.com/cyberforge1) for more projects.
- Or send me an email at obj809@gmail.com
<br />
Thanks for your interest in this project. Feel free to reach out with any thoughts or questions.
<br />
<br />
Oliver Jenkins © 2025
