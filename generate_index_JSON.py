import requests  # Installed
import urllib.parse
import json
from bs4 import BeautifulSoup as Soup  # Installed

wiki_url = "https://wiki.wabbajack.org/"


class IndexedPage(dict):
    def __init__(self, name, href, indexed_headers=None):
        if indexed_headers is None:
            indexed_headers = []
        dict.__init__(self, name=name, href=href, indexed_headers=indexed_headers)


class IndexedHeader(dict):
    def __init__(self, header, href, highlighted_strings=None):
        if highlighted_strings is None:
            highlighted_strings = []
        dict.__init__(self, header=header, href=href, highlighted_strings=highlighted_strings)


def get_html(url):
    return requests.get(url).content


def generate_index(html_item):
    index_helper = []
    chapter = html_item.find("ol", class_="chapter")
    list_items = chapter.find_all('a', href=True)
    for list_item in list_items:
        item_url = list_item['href']
        if item_url[0:1] == "../":
            item_url = item_url.replace("../", "", 1)
        item_url = urllib.parse.quote(item_url)
        full_url = wiki_url + item_url
        print(list_item.get_text() + ":" + full_url)
        indexed_page = IndexedPage(list_item.get_text(),full_url)
        index_helper.append(indexed_page)
    return json.dumps(index_helper)


index_html = Soup(get_html(wiki_url), 'html.parser')

index = generate_index(index_html)

print(index)
