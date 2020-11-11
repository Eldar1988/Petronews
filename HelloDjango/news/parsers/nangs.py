import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://nangs.org/news/world'
HOST = 'https://nangs.org'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='itemContainer')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('h4').find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text().strip()
                slug = get_slug_en(title)
                body = item_soup.find('div', class_='itemFullText')
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 7:
                        break
                    time.sleep(1)
                    continue
            except:
                notification(HOST, f"Error page parse {link}")
                time.sleep(3)
                i = i + 1
                if i > 7:
                    break
                time.sleep(1)
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='Национальная Ассоциация нефтегазового сервиса'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            i = i + 1
            if i > 7:
                break
            time.sleep(1)


def start_parse_nangs():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)