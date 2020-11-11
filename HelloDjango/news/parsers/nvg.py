import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://www.ngv.ru/news/'
HOST = 'http://www.ngv.ru'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('div', class_='news__articles-wrap').find_all('a')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.get('href')
                title = item.find('p').get_text()
                try:
                    image_url = HOST + item.find('img').get('src')
                except:
                    image_url = None
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 7:
                        break
                    time.sleep(1.6)
                    continue
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                body_1 = item_soup.find('p', class_='page-title__subtitle')
                body_2 = item_soup.find('section', class_='post').find('div', class_='post__content-wrap').find('div', class_='post__col').find('article')
                body = str(body_1) + str(body_2)
            except:
                notification(HOST, f"Error page parse {link}")
                time.sleep(1.5)
                i = i + 1
                if i > 7:
                    break
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='Нефтегазовая Вертикаль'
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
            time.sleep(1.5)


def start_parse_nvg():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
