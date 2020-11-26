from news.functions.get_text import get_text
import telebot
from telebot import types

bot = telebot.TeleBot('1432154713:AAFgJXGBPXc_ly3cX53GkdzW88JhhM_6t2Q')
# test
# chat_id = '-1001393981437'
# channel
chat_id = '-1001356024383'


def send_post(post, post_url):
    pass
    keyboard = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(text='Читать новость на сайте', url=post_url)
    keyboard.add(url_btn)
    title = post.title
    body = get_text(post.body)

    print(post_url)
    caption = f'*{title}* \n\n {body[:850]}...'
    bot.send_photo(chat_id, post.image_url, caption=caption, reply_markup=keyboard, parse_mode='Markdown')

