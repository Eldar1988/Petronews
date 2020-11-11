import time
from bs4 import BeautifulSoup

from .constants import get_html
from ..functions.replacer import get_slug_en
from ..models import Post, PostForCompare
from ..notificator import notification

URL = 'https://www.gazprom.ru/press/news/'
HOST = 'https://www.gazprom.ru'


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find('ul', class_='news-list').find_all('li')
    except:
        items = None
        notification(HOST, f"Error start parse {HOST}")
    i = 1
    if items is not None:
        for item in items:
            try:
                link = HOST + item.find('h4').find('a').get('href')
                item_html = get_html(link)
                item_html = item_html.text
                item_soup = BeautifulSoup(item_html, 'html.parser')
                title = item_soup.find('h1').get_text()
                slug = get_slug_en(title)  # Получаем слаг из заголовка
                has_post = PostForCompare.objects.filter(title=title[:55])
                if has_post.count():
                    print('post in base')
                    i = i + 1
                    if i > 3:
                        break
                    time.sleep(3)
                    continue
                try:
                    image_url = HOST + item_soup.find('div', class_='media').find('a').get('href')
                except:
                    image_url = None
                body = item_soup.find('section', class_='content_wrapper')
                try:
                    body_img = body.find_all('div', class_='media')
                    for x in body_img:
                        #  удаляем лишнее
                        ext = x.find('div', class_='ng-hide')
                        ext.extract()
                        ext_desc = x.find('div', class_='desc')
                        ext_desc.extract()
                        #  заменяем ссылки на изображение на полные адреса
                        img = x.find('img')
                        new_src = HOST + img.get('src')
                        img['src'] = new_src

                    #  Находим и удаляем первое изображение
                    body_first_img = body.find('div', class_='media')
                    body_first_img.extract()
                except:
                    body_img = None
                try:
                    stats = body.find_all('div', class_='statistics')
                    for x in stats:
                        x.extract()
                except:
                    stats = None
                try:
                    article_info = body.find('div', class_='article_info')
                    article_info.extract()
                except:
                    article_info = None
                try:
                    article_head = body.find('div', class_='article_head')
                    article_head.extract()
                except:
                    article_head = None
                try:
                    buttons = body.find('div', class_='buttons')
                    buttons.extract()
                except:
                    buttons = None
                try:
                    footer = body.find('div', class_='article_footer')
                    footer.extract()
                except:
                    footer = None
                try:
                    others = body.find('div', class_='other_excusive_reports')
                    others.extract()
                except:
                    others = None
            except:
                notification(HOST, f"Error page parse {link}")
                time.sleep(3)
                i = i + 1
                if i > 3:
                    break
                continue

            try:
                post = Post.objects.create(
                    parse_title=title,
                    title=title,
                    image_url=image_url,
                    body=str(body),
                    source=link,
                    slug=slug,
                    main_source='ГазПром'
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


def start_parse_gazprom():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        notification(HOST, html.status_code)
