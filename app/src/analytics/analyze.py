import psycopg2
import typing as T
import pandas as pd
from textblob import TextBlob

from preprocess import TweetPreprocessor


def get_nrows(table_name: str, conn: psycopg2.extensions.connection) -> int:
    cur = conn.cursor()
    dml = f"""SELECT COUNT(*) FROM {table_name};"""
    cur.execute(dml)
    nrows = cur.fetchone()[0]
    cur.close()
    return nrows


def get_column_values(table: str,
                      column: str,
                      conn: psycopg2.extensions.connection) -> int:
    cur = conn.cursor()
    dml = f"""SELECT {column} FROM {table}"""
    cur.execute(dml)
    results = cur.fetchall()
    cur.close()
    return results


def get_unique_tweet_texts(conn: psycopg2.extensions.connection,
                           tweet_table: str = 'tweets',
                           text_column: str = 'text') -> T.List[str]:
    results = get_column_values(tweet_table, text_column, conn)
    tweet_texts = [t[0] for t in results]
    return list(set(tweet_texts))


def get_sentiment_polarity_df(tweet_texts: T.List[str]) -> pd.DataFrame:
    """Preprocess tweets and analyze polarity"""
    df = pd.DataFrame({'tweet_texts': tweet_texts})

    tweet_preprocessor = TweetPreprocessor()
    df['tweets_cleaned'] = df['tweet_texts'].apply(tweet_preprocessor.preprocess)

    df['sentiment_polarity'] = df['tweet_texts'].apply(lambda x: TextBlob(x).sentiment.polarity)
    return df[['sentiment_polarity']]
