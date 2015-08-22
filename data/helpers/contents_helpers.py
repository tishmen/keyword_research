import re
from collections import Counter
from itertools import tee, islice

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from data.models import Summary, Statistic

NGRAM = 3
LANGUAGE = 'english'
COUNT = 10


# Summary


def summarize(content):
    parser = PlaintextParser.from_string(content.body, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    text = '\n'.join(
        [str(sentence) for sentence in summarizer(parser.document, COUNT)]
    )
    summary = Summary(content=content, summary=text)
    summary.save()


# Statistics

def ngrams(lst, n):
    tlst = lst
    while True:
        a, b = tee(tlst)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tlst = b
        else:
            break


def process(content):
    words = re.findall('\w+', content.body.lower())
    counter = Counter(ngrams(words, NGRAM))
    content.word_count = len(words)
    content.save()
    for item in counter.items():
        keyword = ' '.join(item[0])
        count = item[1]
        statistic = Statistic(
            content=content,
            keyword=keyword,
            count=count,
        )
        statistic.save()
