from django.contrib.auth.models import User
from django.db import models
from HelloDjango.settings import path_and_rename


class Author(models.Model):
    """Автор"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Имя автора', max_length=255)
    avatar = models.ImageField('Аватар (в формате 1:1)', upload_to=path_and_rename('authors/', 'avatar'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
