from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Question(models.Model):
    """Вопрос"""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField('Заголовок', max_length=255)
    body = RichTextUploadingField('Вопрос', blank=True, null=True)
    views = models.PositiveSmallIntegerField('Количество просмотров', default=0)
    public = models.BooleanField('Опубликовать' , default=True)
    pub_date = models.DateTimeField('Дата создания вопроса', auto_now_add=True)
    update = models.DateTimeField('Дата редактировния вопроса', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('-pub_date',)


class Answer(models.Model):
    """Ответ"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL,
                                 related_name='answers', null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name='Ответ на комментарий',
                               on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email', blank=True, null=True)
    text = models.TextField('Текст ответа')
    public = models.BooleanField('Опубликовать', default=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('-pub_date',)
