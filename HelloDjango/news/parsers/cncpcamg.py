import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://www.cnpc-amg.kz/?p=nov_list'
HOST = 'http://www.cnpc-amg.kz/'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('ul', class_='w_newslistpage_list_rus').find_all('li')
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
                title = item_soup.find('div', class_='textbox1').find('p', class_='content_title').get_text().strip()
                print(title)

            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 3:
                    break
                time.sleep(1.5)
                continue

            i = i + 1
            if i > 3:
                break
            time.sleep(1.5)


def start_parse_cnpc_amg():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
