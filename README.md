# Local Database Water Dashboard NSW

## Project Overview
A local MySQL-based water resource management system for tracking and analyzing dam data across New South Wales (NSW), Australia. Built with Python, MySQL, Pandas, and OpenPyXL.


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
The goal of this project is to create a centralized water resource management system that stores dam metadata, tracks real-time water storage levels, archives historical data, and generates analytical reports. By maintaining 24-month rolling historical snapshots and computing rolling averages (12-month, 5-year, 20-year), this system enables trend analysis for individual dams and system-wide metrics across 34 NSW dams.

## Tech Stack
- Python 3
- MySQL 8.0+
- Pandas
- OpenPyXL
- python-dotenv

## How To Use
1. Clone the repository and create a virtual environment with `python3 -m venv venv && source venv/bin/activate`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create a `.env` file with your MySQL credentials (LOCAL_DB_HOST, LOCAL_DB_PORT, LOCAL_DB_NAME, LOCAL_DB_USER, LOCAL_DB_PASSWORD).
4. Run `python3 scripts/local_db_create_db.py` to create the database.
5. Run `python3 scripts/local_db_create_schema.py` to deploy the schema.
6. Run `python3 scripts/local_db_seed_data.py` to seed all data.
7. Export data to Excel with `python scripts/local_export_mysql_to_excel.py`.

## Design Goals
- **Data Integrity**: Enforce referential integrity with foreign keys and cascading relationships.
- **Idempotency**: Use upsert operations (`ON DUPLICATE KEY UPDATE`) for safe re-runs of data seeding.
- **Security**: Prevent SQL injection through parameterized queries with prepared statements.
- **Modularity**: Separate seeding scripts for each table with dependency-ordered execution.

## Project Features
- [x] 34 NSW dams with pre-seeded metadata including capacity, coordinates, and identifiers
- [x] Dam grouping system to categorize dams by type (Sydney, popular, large, small, greatest released)
- [x] Historical data archival with 24 months of monthly snapshots per dam
- [x] Rolling average analysis for per-dam and system-wide metrics
- [x] Excel export utility with timestamped outputs and customizable table filtering
- [x] Parameterized queries for SQL injection prevention
- [x] Foreign key integrity with enforced referential relationships

## Additions & Improvements
- [ ] Integration with live NSW water data APIs
- [ ] Dashboard visualization layer
- [ ] Automated data refresh scheduling
- [ ] Alert thresholds for low storage levels
- [ ] Multi-region support beyond NSW

## Learning Highlights
- Designing normalized database schemas with proper foreign key relationships
- Using mysql-connector-python with parameterized queries for database integration
- Building orchestrated multi-step data pipelines with dependency ordering
- Managing secure credentials with python-dotenv environment configuration
- Implementing upsert patterns, composite keys, and referential integrity in SQL

## Known Issues
- Currently designed for local MySQL instances only; no cloud deployment configuration.
- Seeded data is synthetic with realistic patterns but does not reflect actual NSW dam levels.
- No automated scheduling for data updates; manual refresh required.

## Challenges
- Establishing correct seeding order to satisfy foreign key constraints
- Designing composite primary keys for analysis tables (dam_id, analysis_date)
- Generating realistic synthetic historical data patterns for 24-month archives

## Contact Me
- Visit my [LinkedIn](https://www.linkedin.com/in/obj809/) for more details.
- Check out my [GitHub](https://github.com/cyberforge1) for more projects.
- Or send me an email at obj809@gmail.com
<br />
Thanks for your interest in this project. Feel free to reach out with any thoughts or questions.
<br />
<br />
Oliver Jenkins © 2025