import requests
from bs4 import BeautifulSoup
from readability.readability import Document

from data.models import Link, Content


def scrape(result):
    start_url = result.url
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    document = Document(response.content)
    body_soup = BeautifulSoup(document.summary(), 'html.parser')
    links = [Link(url=el['href']) for el in soup.select('a') if el.get('href')]
    for link in links:
        link.save()
    content = Content(
        result=result,
        html=soup.prettify(),
        title=document.short_title(),
        body_html=body_soup.prettify(),
        body=body_soup.get_text(),
    )
    content.save()
    content.links.add(*links)
