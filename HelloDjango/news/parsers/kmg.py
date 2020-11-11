import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError, NewConnectionError

from ..functions.replacer import get_slug_en
from ..models import PostForCompare, Post
from ..notificator import notification

URL = 'https://www.kmg.kz/rus/press-centr/press-relizy/'
HOST = 'https://www.kmg.kz'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': UserAgent().chrome
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='item')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = URL + item.find('div', class_='text').find('h3').find('a').get('href')
                item_html = get_html(link).text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                parse_title = item_soup.find('h3', class_='title').get_text()
                body = item_soup.find('div', class_='full')
                try:
                    image_url = HOST + item_soup.find('div', class_='block').find('a').get('href')
                except:
                    image_url = None
                slug = get_slug_en(parse_title)
                has_post = PostForCompare.objects.filter(title=parse_title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 8:
                        break
                    time.sleep(3)
                    continue
            except:
                notification(HOST, f"Error page parse {link}")
                time.sleep(3)
                continue

            try:
                post = Post.objects.create(
                    parse_title=parse_title,
                    title=parse_title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='КазМунайГаз'
                )
                post.save()

                compare_title = parse_title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            i += i
            if i > 8:
                break
            time.sleep(5)


def start_parse_kmg():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
