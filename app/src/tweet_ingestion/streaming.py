import json
import tweepy
import yaml
import psycopg2
import logging
import typing as T

import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('twitter_streaming_logger')


def extract_tweet_variables(tweet_json: 'tweet._json',
                            columns: T.List[str]) -> T.List[T.Any]:
    """Extract pre-defined variables from tweet object's _json fields"""
    variables = []
    for col in columns:
        # renamed user as user_account due to postgre's naming convention
        if col == 'user_account':
            col = 'user'

        if col in tweet_json:
            if type(tweet_json[col]) == dict:
                variables.append(json.dumps(tweet_json[col]))
            else:
                variables.append(tweet_json[col])
        else:
            variables.append(None)

    return variables


def insert_new_row(table: str, columns: T.List[str], variables: T.List[T.Any],
                   conn: psycopg2.extensions.connection):
    columns_str = ', '.join(columns)
    placeholders_str = ('%s,' * len(columns))[:-1]
    dml = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders_str})"

    cur = conn.cursor()
    cur.execute(dml, variables)
    conn.commit()
    cur.close()


# Create a StreamListner class
# override tweepy.StreamListener to add logic to on_status
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        for word in settings.TRACK_WORDS:
            # Use full text of tweet if applicable
            if hasattr(status, 'extended_tweet'):
                status._json['text'] = status.extended_tweet['full_text']
            elif hasattr(status, 'retweeted_status') and hasattr(status.retweeted_status, 'extended_tweet'):
                status._json['text'] = status.retweeted_status.extended_tweet['full_text']

            # Store the tweet if its text contains any track word
            if word.lower() in status._json['text'].lower():
                variables = extract_tweet_variables(status._json, columns)
                try:
                    insert_new_row('tweets', columns, variables, conn)
                    logger.info(status._json['text'])
                except Exception as e:
                    logger.warning(f'Failed to insert row: {str(e)}')
                    conn.rollback()

                break

    def on_error(self, status_code):
        """Stop calling Twitter api when exceed calling limit"""
        if status_code == 420:
            # Disconnect the stream
            logger.warning('Disconnect the stream due to API calling threshold, status code: {420}')
            return False


if __name__ == '__main__':
    # Authenticate api
    with open('app/src/tweet_ingestion/twitter_credentials.json', 'r') as h:
        twitter_dev_accounts = json.load(h)
    credentials = twitter_dev_accounts[0]

    auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token_key'], credentials['access_token_secret'])
    api = tweepy.API(auth)

    # Connect to db
    conn = psycopg2.connect(dbname='stream_tweets')

    # Load columns for tweet table
    schemas_path = 'app/src/tweet_ingestion/schemas.yaml'
    with open(schemas_path) as stream:
        schemas = yaml.safe_load(stream)
    columns = schemas[-1]['columns']

    # Create StreamListener object
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # Start streaming
    logger.info('Start streaming')
    myStream.filter(languages=["en"], track=settings.TRACK_WORDS)

