import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.bp.com/en/global/corporate/news-and-insights.html#searchCards-news-and-insights'
HOST = 'https://www.bp.com'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='fade-enter-done')
        print(items)
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = item.find('a').get('href')
                print(link)

            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 6:
                    break
                time.sleep(3)
                continue


def start_parse_bp():
    html = get_html(URL)
    time.sleep(7)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
