import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def extract_url(url):
    query = urlparse(url).query
    query_parsed = parse_qs(query)
    return query_parsed['q'][0]


def scrape(keyword):
    start_url = 'https://www.google.com/search?q={}'.format(keyword)
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for i, link in enumerate(soup.select('.g > .r a')):
        result = {
            'keyword': keyword,
            'url': extract_url(link['href']),
            'position': i + 1,
        }
        results.append(result)
    return results