import psycopg2
from typing import List, Tuple, Any


def get_all_tables(connection: psycopg2.extensions.connection) -> List[str]:
    c = connection.cursor()
    dml = f"""SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'"""
    c.execute(dml)
    results = c.fetchall()
    c.close()
    return [result[0] for result in results]


def get_nrows(table: str, conn: psycopg2.extensions.connection) -> int:
    cur = conn.cursor()
    dml = f"""SELECT COUNT(*) FROM {table}"""
    cur.execute(dml)
    result = cur.fetchone()
    cur.close()
    return result[0]


def get_first_row(name: str, connection: psycopg2.extensions.connection) -> Tuple[Any]:
    cur = connection.cursor()
    dml = f"""SELECT * FROM {name};"""
    cur.execute(dml)
    first_row = cur.fetchone()
    cur.close()
    return first_row


def drop_table(name: str, connection: psycopg2.extensions.connection):
    cur = connection.cursor()
    ddl = f"""DROP TABLE {name}"""
    cur.execute(ddl)
    connection.commit()
    cur.close()
