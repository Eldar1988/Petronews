import re
import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.shell.com/'
HOST = 'https://www.shell.com'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('div', class_='reference').find_all('div', class_='promo-list__item')

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
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    time.sleep(3)
                    continue
                body_1 = item_soup.find('div', class_='page-header__text')
                body_1_date = body_1.find('p', class_='page-header__date')
                body_1_date.extract()
                body_2 = item_soup.find_all('div', class_='textimage')
                body = str(body_1)
                for i in body_2:
                    body = str(body) + str(i)
            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 3:
                    break
                time.sleep(1.5)
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='Shell'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            time.sleep(1.5)


def start_parse_shell():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
