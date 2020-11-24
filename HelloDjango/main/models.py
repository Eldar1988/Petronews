from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from HelloDjango.settings import path_and_rename


class MainInfo(models.Model):
    """Основная информация"""
    title = models.CharField('Title сайта', max_length=255)
    description = models.TextField('Description', max_length=180, help_text='до 180 символово')
    favicon = models.ImageField('Иконка сайта', upload_to=path_and_rename('main/', 'favicon'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заголовок, описание и иконка'
        verbose_name_plural = 'Заголовок, описание и иконка'


class Contacts(models.Model):
    """Контакты"""
    address = models.TextField('Адрес', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Social(models.Model):
    """Социальные сети"""
    name = models.CharField('Название сати', max_length=255)
    icon = models.TextField('Иконка', help_text='https://fontawesome.com/icons?d=gallery')
    url = models.CharField('Ссылка на страницу в сети', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'


class Footer(models.Model):
    """Footer info"""
    text_one = models.TextField('Информация в первой колонке футера', blank=True)
    text_two = models.TextField('Информация во второй колонке футера', blank=True)
    copyright = models.CharField('Копирайт', max_length=255, blank=True)

    def __str__(self):
        return self.copyright

    class Meta:
        verbose_name = 'Информация в футере сайта'
        verbose_name_plural = 'Информация в футере сайта'


class Politic(models.Model):
    """Политика конфиденциальности"""
    title = models.CharField('Заголовок', max_length=255)
    text = RichTextUploadingField('Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'


class About(models.Model):
    """Политика конфиденциальности"""
    title = models.CharField('Заголовок', max_length=255)
    text = RichTextUploadingField('Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Инофрмация о проекте'
        verbose_name_plural = 'Инофрмация о проекте'

#
# class TgBot(models.Model):
#     """Телеграм бот"""
#     url = models.CharField(max_length=255)
#     chat_id = models.CharField(max_length=30)
#     token = models.CharField(max_length=200, null=True)
#     text_len = models.PositiveSmallIntegerField('Длина текста', null=True, blank=True, default=30)
#
#
#
#     def __str__(self):
#         return self.chat_id
#
#     class Meta:
#         verbose_name = 'Телеграм бот'
#         verbose_name_plural = 'Телеграм боты'


class Course(models.Model):
    """курсы валют"""
    usd = models.CharField('Курс доллара', null=True, blank=True, max_length=10)
    eur = models.CharField('Курс евро', null=True, blank=True, max_length=10)
    rub = models.CharField('Курс рубля', null=True, blank=True, max_length=10)