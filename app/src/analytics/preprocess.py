import typing as T
import preprocessor as tweet_cleaner

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r"[a-zA-Z]{2,}")
lemmatizer = WordNetLemmatizer()


class TweetPreprocessor:
    """Further preprocess tweet text for downstream tasks"""

    def __init__(self, tweet_cleaner=tweet_cleaner, tokenizer=tokenizer,
                 lemmatizer=lemmatizer, stopwords=stop_words):
        self.tweet_cleaner = tweet_cleaner
        self.tokenizer = tokenizer
        self.lemmatizer = lemmatizer
        self.stopwords = stopwords

    def _remove_stopwords(self, tokens: T.Tuple[str]) -> T.Tuple[str]:
        return [x for x in tokens if x not in self.stopwords]

    def _lemmatize(self, tokens: T.Tuple[str]) -> T.Tuple[str]:
        return [self.lemmatizer.lemmatize(x) for x in tokens]

    def preprocess(self, text: str) -> str:
        text = text.lower()
        # Keep meaningful text only: https://github.com/s/preprocessor
        text_cleaned = self.tweet_cleaner.clean(text)
        tokens = self.tokenizer.tokenize(text_cleaned)
        tokens = self._remove_stopwords(tokens)
        tokens = self._lemmatize(tokens)
        return ' '.join(tokens)
