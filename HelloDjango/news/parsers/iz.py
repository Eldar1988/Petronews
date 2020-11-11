import re
import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://iz.ru/tag/neft'
HOST = 'https://iz.ru'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='lenta_news__day')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text().strip()
                body = item_soup.find('article')


            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 5:
                    break
                time.sleep(1.5)
                continue

            i = i + 1
            if i > 4:
                break
            time.sleep(1.5)


def start_parse_iz():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
