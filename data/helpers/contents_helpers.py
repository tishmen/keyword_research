import re
from collections import Counter
from itertools import tee, islice

from data.models import Statistic


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
    counter = Counter(ngrams(words, 3))
    for item in counter.items():
        keyword = ' '.join(item[0])
        count = item[1]
        statistic = Statistic(
            content=content,
            keyword=keyword,
            count=count,
        )
        statistic.save()
