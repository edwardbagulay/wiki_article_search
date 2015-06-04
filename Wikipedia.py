import requests
from exceptions import Exception
from bs4 import BeautifulSoup

def Wikipedia(article):
#    url = "http://en.wikipedia.org/wiki/"
    query = {
        "search": article,
        "title": "Special:Search",
        "go": "Go"
    }
    url = "http://en.wikipedia.org/w/index.php"

    html = requests.get(url, params=query).text
    soup = BeautifulSoup(html)

    if is_disambiguation_page(soup):
        raise Exception("Disambiguation page") 

    if is_search_page(soup):
        raise Exception("Search found no article")

    title = soup.find('h1', { "id" : "firstHeading" })
    summary = soup.find('div', { "id" : "mw-content-text" }).find('p')

    for sup in summary.findAll('sup', { "class" : "reference" }):
        sup.extract()

    return {
        "title" : title.string,
        "summary": summary.getText()
    }

def is_disambiguation_page(soup):
    if soup.find('table', { "id" : "disambigbox" }) is not None:
        return True
    else:
        return False

def is_search_page(soup):
    if soup.find('p', { "class" : "mw-search-createlink" }) is not None:
        return True
    else:
        return False
