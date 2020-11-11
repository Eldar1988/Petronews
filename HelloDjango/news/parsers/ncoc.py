import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.ncoc.kz/'
HOST = 'https://www.ncoc.kz/'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        item = soup.find('div', {'data-bind': 'foreach:LatestNews'})
        print(item)
    except:
        item = None
        notification(HOST, f"Error start parse {HOST}")






def start_parse_ncoc():
    html = get_html(URL)
    time.sleep(3)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
