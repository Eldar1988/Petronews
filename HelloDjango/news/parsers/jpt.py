import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://pubs.spe.org/en/jpt/jpt-main-page/'
HOST = 'https://pubs.spe.org'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('article', class_='story')
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
                title = item_soup.find('h2', class_='tiletitles').get_text().strip()
                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 3:
                        break
                    time.sleep(1)
                    continue
                try:
                    image_url = HOST + item_soup.find('div', class_='articlePicture').find('img').get('src')
                except:
                    image_url = None
                body = item_soup.find('div', class_='articleBodyText')
                try:
                    body_ings = body.find_all('img')
                    for p in body_ings:
                        p_link = HOST + p.get('src')
                        p['src'] = p_link
                        print(p)
                except:
                    body_ings = None

            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 3:
                    break
                time.sleep(1)
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='JPT'
                )
                post.save()

                compare_title = title[:55]
                compare_post = PostForCompare.objects.create(
                    title=compare_title
                )
                compare_post.save()
            except:
                notification(HOST, f"Can't to create Post. Parse content - {link}")

            i += 1
            if i > 3:
                break
            time.sleep(1.5)


def start_parse_jpt():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
