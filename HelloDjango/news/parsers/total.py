import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.total.com/media/press-releases'
HOST = 'https://www.total.com'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('article')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('h2').find('a').get('href')
                image_url = HOST + item.find('img').get('src')
                title = item.find('h2').get_text().strip()
                slug = get_slug_en(title)
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                body = item_soup.find('article')
                body_date = body.find('div', class_='tab-content')
                body_date.extract()
                try:
                    body_img = body.find_all('img')
                    for x in body_img:
                        x.extract()
                except:
                    body_img = None
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 3:
                        break
                    time.sleep(3)
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
                    main_source='Total'
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
            if i > 3:
                break
            time.sleep(3)
            continue


def start_parse_total():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)

