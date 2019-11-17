# twitter-real-time-keyword-tracking
App for tracking and analysing tweets that contain interested keywords in real-time. It's built to provide insights for brand analytics and stock price prediction.


# Quick Start
#### Set up environment
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
    createdb stream_tweets
    # Create tables
    python app/src/tweet_ingestion/create_tables.py

#### Set up twitter credentials

#### Set up word to be tracked

#### Fetching streaming tweets
    
    python app/src/tweet_ingestion/streaming.py
    
#### Launch the analytics APP

    python app/src/analytics/dash_app.py
