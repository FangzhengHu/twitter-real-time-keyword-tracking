# alternative-data-system
A system that collect, process, and analyse alternative data in real-time to provide insights for investment.

Data sources included:
- twitter
# Quick Start
### Set up environment
Install dependent python packages

    pipenv sync
    pipenv shell
Install and start database server
    
    # Install Postgres
    brew install postgres  
    # Start PostgreSQL server
    pg_ctl -D /usr/local/var/postgres start
    # Create a database cluster
    initdb /usr/local/var/postgres
    # Start server
    pg_ctl -D /usr/local/var/postgres -l logfile start

Create database and tables

    # Create database
    createdb alternative_data
    # Create tables
    python src/create_tables.py

### Set up twitter credentials

### Set up word to be tracked
