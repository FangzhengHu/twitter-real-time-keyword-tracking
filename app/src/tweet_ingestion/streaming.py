from typing import List, Any
import psycopg2
import json


def extract_tweet_variables(tweet_json: 'tweet._json',
                            columns: List[str]) -> List[Any]:
    """Extract pre-defined variables from tweet object's _json fields"""
    variables = []
    for var in columns:
        # renamed user as user_account due to postgre's naming convention
        if var == 'user_account':
            var = 'user'

        if var in tweet_json:
            if type(tweet_json[var]) == dict:
                variables.append(json.dumps(tweet_json[var]))
            else:
                variables.append(tweet_json[var])
        else:
            variables.append(None)

    return variables


def insert_new_row(table: str, columns: List[str], variables: List[Any],
                   conn: psycopg2.extensions.connection):
    columns_str = ', '.join(columns)
    placeholders_str = ('%s,' * len(columns))[:-1]
    dml = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders_str})"

    cur = conn.cursor()
    cur.execute(dml, variables)
    conn.commit()
    cur.close()
