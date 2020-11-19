from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'public', 'pub_date')
    list_editable = ('public',)
    search_fields = ('title',)

    save_as = True


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'public')
    list_editable = ('public',)
    search_fields = ('question',)

    save_as = True
