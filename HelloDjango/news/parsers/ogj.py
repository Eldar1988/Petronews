import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.ogj.com/'
HOST = 'https://www.ogj.com'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('li', class_='item-list__item')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = item.find('h5', class_='item__title').find('a').get('href')
                link_f = link.find('http')
                if link_f == 0:
                    time.sleep(1.5)
                    continue
                link = HOST + link
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text()
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 30:
                        break
                    time.sleep(3)
                    continue
                try:
                    image_url = item_soup.find('div', class_='page-body-image').find('img').get('src')
                except:
                    image_url = None
                body_1 = item_soup.find('p', class_='page-wrapper__deck')
                body_2 = item_soup.find('div', class_='content-body-contents')
                body = str(body_1) + str(body_2)
            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 30:
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
                    main_source='Oil&Gas Journal'
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
            if i > 30:
                break
            time.sleep(1.5)
            continue


def start_parse_ogj():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
