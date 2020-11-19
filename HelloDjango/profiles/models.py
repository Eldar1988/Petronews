from django.contrib.auth.models import User
from django.db import models
from HelloDjango.settings import path_and_rename
from django.shortcuts import redirect
from django.urls import reverse


class Author(models.Model):
    """Автор"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField('Имя автора', max_length=255, default='User', blank=True, null=True)
    last_name = models.CharField('Фамилия автора', max_length=255, blank=True, null=True)
    professional = models.CharField('Профессия', max_length=255, null=True, blank=True)
    avatar = models.ImageField('Аватар (в формате 1:1)', upload_to=path_and_rename('authors/', 'avatar'), blank=True,
                               null=True)
    background = models.ImageField('Фоновое изображение профиля', upload_to=path_and_rename('authors/', 'bg'),
                                   blank=True, null=True)
    bio = models.TextField('Bio', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
