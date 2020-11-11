import requests
import time
from bs4 import BeautifulSoup

from ..functions.replacer import get_slug_en
from ..models import PostForCompare, Post
from ..notificator import notification

URL = 'https://neftegaz.ru/news/'
HOST = 'https://neftegaz.ru'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='news_week__item')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                item_url = item.find('div', class_='info').find('div', class_='title').find('a').get('href')
                item_html = get_html(item_url)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('div', class_='title').find('h1').get_text()
                try:
                    image_url = HOST + item_soup.find('img', itemprop='image').get('src')
                except:
                    image_url = None
                if image_url is None:
                    time.sleep(3)
                    try:
                        image_url = HOST + item_soup.find('a', class_='slick-slide').find('img').get('src')
                    except:
                        image_url = None
                body1 = item_soup.find('div', class_='text')
                body = body1
                slug = get_slug_en(title)

                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('This theme is in database')
                    i = i + 1
                    if i > 10:
                        break
                    time.sleep(3)
                    continue
            except:
                notification(HOST, f"Error page parse {item_url}")
                time.sleep(2)
                continue
            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=item_url,
                    slug=slug,
                    main_source='Neftegaz.ru'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {item_url}")

            i = i + 1
            if i > 10:
                break
            time.sleep(2)


def start_parse_neftegaz():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
