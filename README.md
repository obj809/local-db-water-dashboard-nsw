# Local Database Water Dashboard NSW

## Project Overview
A local MySQL-based system for tracking and analyzing dam data across NSW, Australia. Features an ETL pipeline that transforms raw WaterNSW API data and loads it into a normalized database schema.

## Table of Contents

- [Tech Stack](#tech-stack)
- [How To Use](#how-to-use)
- [Project Architecture](#project-architecture)
- [Design Goals](#design-goals)
- [Project Features](#project-features)
- [Learning Highlights](#learning-highlights)
- [Known Issues](#known-issues)
- [Challenges](#challenges)

![Database schema](database-schema.png)

## Goals & MVP
Create a centralized system that stores dam metadata, tracks water storage levels, archives historical data, and supports analytical reporting for 38 NSW dams.

## Tech Stack
- Python 3
- MySQL 8.0+
- Pandas
- OpenPyXL
- python-dotenv

## How To Use

### 1. Environment Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Database
Create `.env` file with MySQL credentials:
```
LOCAL_DB_HOST=127.0.0.1
LOCAL_DB_PORT=3306
LOCAL_DB_NAME=water_dashboard_nsw_local
LOCAL_DB_USER=your_user
LOCAL_DB_PASSWORD=your_password
```

### 3. Database Setup
```bash
python3 scripts/local_db_create_db.py
python3 scripts/local_db_create_schema.py --force
```

### 4. ETL Pipeline
```bash
# Transform raw data
python3 transform/transform_dams.py
python3 transform/transform_latest_data.py
python3 transform/transform_dam_resources.py
python3 transform/transform_dam_groups.py
python3 transform/transform_dam_group_members.py

# Seed database
python3 scripts/local_db_seed_data.py
```

### 5. Export to Excel
```bash
python scripts/local_export_mysql_to_excel.py
```

## Project Architecture

```
├── input_data/           # Raw JSON data from WaterNSW API
│   ├── dams.json
│   ├── dams_resources_latest.json
│   └── dam_resources/    # Historical data per dam
├── transform/            # ETL transform scripts
├── output_data/          # Transformed data (schema-ready)
├── seeding/              # Database seeding scripts
├── scripts/              # DB setup and export utilities
├── queries/              # Example SQL queries
└── schema.sql            # Database schema definition
```

### Data Flow
```
WaterNSW API → input_data/ → transform/ → output_data/ → seeding/ → MySQL
```

## Design Goals
- **Data Integrity**: Foreign keys with cascading relationships
- **Idempotency**: Upsert operations for safe re-runs
- **Security**: Parameterized queries to prevent SQL injection
- **Modularity**: Separate transform and seeding scripts with dependency ordering

## Project Features
- [x] 38 NSW dams with metadata (capacity, coordinates, identifiers)
- [x] Dam grouping system (Sydney, popular, large, small, greatest released)
- [x] Historical monthly snapshots from WaterNSW API
- [x] ETL pipeline for data transformation
- [x] Excel export with customizable table filtering

## Learning Highlights
- ETL pipeline design with separation of concerns
- Normalized database schema design with foreign key relationships
- Orchestrated data pipelines with dependency ordering
- Upsert patterns and composite keys in SQL

## Known Issues
- Local MySQL only; no cloud deployment configuration
- Manual refresh required; no automated scheduling

## Challenges
- Establishing correct seeding order for foreign key constraints
- Designing composite primary keys for analysis tables
- Transforming nested API responses to flat schema-ready format

## Contact Me
- Visit my [LinkedIn](https://www.linkedin.com/in/obj809/) for more details.
- Check out my [GitHub](https://github.com/cyberforge1) for more projects.
- Or send me an email at obj809@gmail.com

Thanks for your interest in this project. Feel free to reach out with any thoughts or questions.

Oliver Jenkins © 2025
