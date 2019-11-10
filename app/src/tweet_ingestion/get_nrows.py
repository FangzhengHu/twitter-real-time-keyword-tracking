import argparse
import psycopg2
import db_utils as dbu


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', default='tweets', type=str)
    args = parser.parse_args()

    conn = psycopg2.connect(dbname='alternative_data')
    nrows = dbu.get_nrows(args.table, conn)
    print(f'nrows: {nrows}')
