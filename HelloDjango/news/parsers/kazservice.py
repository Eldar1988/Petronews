import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://kazservice.kz/info/news'
HOST = 'http://kazservice.kz'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('div', class_='single-new')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('a', class_='button-primary').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text()
                try:
                    image_url = HOST + item_soup.find('div', class_='detail').find('img').get('src')
                except:
                    image_url = None
                body = item_soup.find('div', class_='content')
                body_wthout_img = body.find_all('img')
                for x in body_wthout_img:
                    x.extract()
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    time.sleep(3)
                    i = i + 1
                    if i > 5:
                        break
                    continue
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
                    main_source='KazService'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't ot create Post. Parse content - {link}")
            i = i + 1
            if i > 5:
                break

            time.sleep(3)


def start_parse_kazservice():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
