import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://www.tengizchevroil.com/about/media/tconews/'
HOST = 'https://www.tengizchevroil.com'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('li', class_='item')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = item.find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('div', class_='blog-detail').find('h2').find('span').get_text().strip()
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 1:
                        break
                    time.sleep(1.5)
                    continue
                try:
                    image_url = HOST + item_soup.find('div', class_='body').find('img').get('src')
                except:
                    image_url = None
                body = item_soup.find('div', class_='body')
                try:
                    body_imgs = body.find_all('img')
                    for i in body_imgs:
                        i.extract()
                except:
                    body_first_img = None
            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 1:
                    break
                time.sleep(1.5)
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='Тенгиз Шевроил'
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
            if i > 1:
                break
            time.sleep(1.5)
            continue


def start_parse_tengizchevroil():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
