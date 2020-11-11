import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.kpo.kz/ru/novosti.html'
HOST = 'https://www.kpo.kz/ru'
LINK_HOST = 'https://www.kpo.kz/'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('div', class_='p_content').find_all('span', class_='p_content_title')
    except:
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = LINK_HOST + item.find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('div', class_='news-single-item-title').find('span').get_text()
                try:
                    image_url = LINK_HOST + item_soup.find('div', class_='news-single-img').find('img').get('src')
                except:
                    image_url = None
                body = item_soup.find('div', class_='news-single-item')
                body_title = body.find('div', class_='news-single-item-title')
                body_title.extract()
                body_date = body.find('div', class_='news-single-rightbox')
                body_date.extract()
                body_share = body.find('div', class_='yashare-auto-init')
                body_share.extract()
                body_next = body.find('div', class_='news-single-backlink-main')
                body_next.extract()
                body_img_ex = body.find_all('img')
                for x in body_img_ex:
                    x.extract()

                slug = get_slug_en(title)
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 4:
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
                    main_source='Karachaganak'
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
            time.sleep(3)


def start_parse_kpo():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)