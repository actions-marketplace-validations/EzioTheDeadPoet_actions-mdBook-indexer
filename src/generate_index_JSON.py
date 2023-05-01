import os
import sys
import requests  # Installed
import urllib.parse
import json
from pathlib import Path
from bs4 import BeautifulSoup as Soup  # Installed

if len(sys.argv) < 2:
    print("missing arguments: mbBook_url output_file(optional)")
    exit(-1)

mdBook_url = sys.argv[1]

output_file = "mbBook_index.json"

if len(sys.argv) >= 3:
    output_file = sys.argv[2]


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


def generate_page_index(file_url):
    html_item = Soup(get_html(file_url), 'html.parser')
    indexed_pages_helper = []
    chapter = html_item.find("ol", class_="chapter")
    list_items = chapter.find_all('a', href=True)
    for list_item in list_items:
        item_url = list_item['href']
        item_url = urllib.parse.quote(item_url)
        full_url = file_url + item_url
        indexed_page = IndexedPage(list_item.get_text(), full_url, generate_indexed_headers(full_url))
        indexed_pages_helper.append(indexed_page)
    return json.dumps(indexed_pages_helper, indent=2)


def generate_indexed_headers(file_url):
    html_item = Soup(get_html(file_url), 'html.parser')
    indexed_headers_helper = []
    content = html_item.find("div", class_="content")
    main = content.main
    highlighted_strings = []
    all_in_main = main.find_all(search_condition)
    all_in_main.reverse()
    for found_item in all_in_main:
        if is_header(found_item):
            item_url = found_item.a['href']
            item_url = urllib.parse.quote(item_url, '/#')
            full_url = file_url + item_url
            indexed_page = IndexedHeader(found_item.a.get_text(), full_url, highlighted_strings)
            indexed_headers_helper.append(indexed_page)
            highlighted_strings = []

        highlighted_strings.append(found_item.get_text())
    return indexed_headers_helper


def is_header(element):
    if element.a is None:
        return False
    header_link = element.a
    return header_link.has_attr('class') and header_link['class'].count('header') > 0


def search_condition(element):
    if element.name == "strong" or element.name == "code" or is_header(element):
        return True
    return False


print("The indexed data will be stored into:\n"+output_file)

p = Path(os.path.dirname(output_file))
p.mkdir(exist_ok=True)

with open(output_file, "w") as outfile:
    outfile.write(generate_page_index(mdBook_url))
    print("Indexing complete.\n")
