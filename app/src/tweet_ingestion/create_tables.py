import argparse
import psycopg2
import yaml
from db_utils import get_all_tables, drop_table


def create_table(name: str, schema: str,
                 connection: psycopg2.extensions.connection):
    c = connection.cursor()
    ddl = f"""CREATE TABLE IF NOT EXISTS {name} ({schema})"""
    c.execute(ddl)
    connection.commit()
    c.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', default=0, type=int)
    args = parser.parse_args()

    schemas_path = './configs/schemas.yaml'
    with open(schemas_path) as stream:
        schemas = yaml.safe_load(stream)

    conn = psycopg2.connect(dbname='alternative_data')

    # Drop existing tables
    if args.reset:
        tables = get_all_tables(conn)
        for table in tables:
            drop_table(table, conn)

    for schema in schemas:
        create_table(schema['name'], schema['schema'], conn)



