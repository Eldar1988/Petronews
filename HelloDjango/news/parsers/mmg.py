import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'http://www.mmg.kz/page.php?page_id=11&lang=1'
URL_TO_LINK = 'http://www.mmg.kz/page.php?page_id=11&lang=1/'
HOST = 'http://www.mmg.kz/'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all('td', class_='nw3')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = URL + item.find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('td', class_='nw1').get_text()
                try:
                    image_url = HOST + item_soup.find('td', class_='td4').find('img').get('src')
                except:
                    image_url = None
                body = item_soup.find('td', class_='nw2')
                body_wthout_img = body.find_all('img')
                for x in body_wthout_img:
                    x.extract()
                slug = get_slug_en(title)
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
                time.sleep(3)
                continue
            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title[11:],
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug[9:-2],
                    main_source='МангистауМунайГАз'
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

            i = i + 1
            if i > 5:
                break


def start_parse_mmg():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
