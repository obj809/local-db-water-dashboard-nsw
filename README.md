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

## Additions & Improvements
- [ ] Live NSW water data API integration
- [ ] Dashboard visualization layer
- [ ] Automated data refresh scheduling
- [ ] Low storage level alerts
- [ ] Multi-region support

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

## Contact Me
- Visit my [LinkedIn](https://www.linkedin.com/in/obj809/) for more details.
- Check out my [GitHub](https://github.com/cyberforge1) for more projects.
- Or send me an email at obj809@gmail.com
<br />
Thanks for your interest in this project. Feel free to reach out with any thoughts or questions.
<br />
<br />
Oliver Jenkins © 2025
