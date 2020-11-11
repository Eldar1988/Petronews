import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.kaztransgas.kz/index.php/ru/press-tsentr/novosti-kompanii'
HOST = 'https://www.kaztransgas.kz'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='span6')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('p', class_='readmore').find('a', class_='btn').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('div', class_='page-header').find('h2').get_text()
                body = item_soup.find('div', {'itemprop': 'articleBody'})
                try:
                    image_url = HOST + body.find('img').get('src')
                except:
                    image_url = None
                slug = get_slug_en(title)
                body_wthout_img = body.find('img')
                body_wthout_img.extract()
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 6:
                        break
                    time.sleep(3)
                    continue
            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 6:
                    break
                time.sleep(3)
                continue
            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='КазТрансГаз'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            time.sleep(3)


def start_parse_kaztransgaz():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
