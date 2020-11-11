import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://energynow.ca/news/'
HOST = 'https://energynow.ca'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('div', class_='entry-content').find_all('li')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = item.find('a').get('href')
                image_url = item.find('img').get('src')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text().strip()
                slug = get_slug_en(title)
                body = item_soup.find('div', class_='entry-content')
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 15:
                        break
                    time.sleep(1)
                    continue
                try:
                    body_grid = body.find('div', class_='grid-container')
                    body_grid.extract()
                except:
                    body_grid = None
                try:
                    body_ext_1 = body.find('div', class_='addtoany_shortcode')
                    body_ext_1.extract()
                except:
                    body_ext_1 = None
                try:
                    body_ext_2 = body.find('h4')
                    body_ext_3 = body_ext_2.findNext('div')
                    body_ext_2.extract()
                    body_ext_3.extract()
                except:
                    body_ext_2 = None
            except:
                notification(HOST, f"Error page parse {link}")
                i += 1
                if i > 3:
                    break
                time.sleep(15)
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='EnergyNow'
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
            if i > 15:
                break


def start_parse_energynow():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)