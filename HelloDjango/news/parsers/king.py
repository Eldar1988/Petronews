import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://www.king.kz/news'
HOST = 'http://www.king.kz'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='our-news-item')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('a').get('href')
                if link == 'http://www.king.kz/news/news_15092020':
                    print('post in base')
                    i = i + 1
                    time.sleep(1)
                    if i > 10:
                        break
                    continue
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h3').get_text()
                try:
                    image_url = HOST + item_soup.find('div', class_='main__section1__block1').find('img').get('src')
                except:
                    image_url = None
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:255])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 10:
                        break
                    time.sleep(3)
                    continue
                body = item_soup.find('div', class_='main__section1__block2')
                body_header = body.find('h3')
                body_header.extract()
            except:
                notification(HOST, f"Error page parse {link}")
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
                    main_source='KING'
                )
                post.save()

                compare_title = title[:255]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            i = i + 1
            if i > 10:
                break
            time.sleep(3)


def start_parse_king():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
