import io
from news.functions.get_text import get_text
import requests
import telebot
from telebot import types

from .models import TgBot

bot_model = TgBot.objects.last()

bot = telebot.TeleBot(bot_model.token)
chat_id = bot_model.chat_id


def send_post(post, post_url):
    keyboard = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(text='Читать новость на сайте', url=post_url)
    keyboard.add(url_btn)
    title = post.title
    body = get_text(post.body)
    print(bot_model.text_len)
    caption = f'*{title}* \n\n {body[:bot_model.text_len]}...'
    bot.send_photo(chat_id, post.image_url, caption=caption, reply_markup=keyboard, parse_mode='Markdown')

