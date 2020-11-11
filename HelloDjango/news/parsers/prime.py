import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://1prime.ru/oil/'
HOST = 'https://1prime.ru'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('div', class_='rubric-list__articles').find_all('article')
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
                title = item_soup.find('h1').get_text()
                try:
                    image_url = HOST + item_soup.find('figure', class_='article-header__media').find('img').get('src')
                except:
                    image_url = None
                slug = get_slug_en(title)
                body = item_soup.find('div', class_='article-body')
                try:
                    inject = body.find_all('section', class_='inject-article')
                    for x in inject:
                        x.extract()
                except:
                    inject = None
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 5:
                        break
                    time.sleep(1.5)
                    continue
            except:
                notification(HOST, f"Error page parse {link}")
                i = i + 1
                if i > 5:
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
                    main_source='Прайм'
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
            if i > 5:
                break
            time.sleep(1.5)


def start_parse_prime():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
