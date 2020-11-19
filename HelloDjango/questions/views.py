from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import Question, Answer
from .functions.q_paginator import get_pagination
from .forms import QuestionForm, AnswerForm


def questions_list(request):
    """Список вопросов"""
    questions = Question.objects.filter(public=True).defer('body', 'update')
    context = get_pagination(request, questions)
    popular_questions = Question.objects.filter(public=True).defer('body', 'update').order_by('-views')[:7]
    context['populars'] = popular_questions
    return render(request, 'questions/questions_list.html', context)


class QuestionDetailView(View):
    """Детали вопрсоа"""
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        popular_questions = Question.objects.filter(public=True).defer('body', 'update').order_by('-views')[:8]
        answers = Answer.objects.filter(question_id=pk)
        return render(request, 'questions/question_detail.html', {
            'question': question,
            'popular_questions': popular_questions,
            'answers': answers,
        })


class AddAnswer(View):
    """Ответ на вопрос"""
    def post(self, request, pk):
        form = AnswerForm(request.POST)
        answer = Answer.objects.filter(text__icontains=request.POST.get('text'))
        if answer.count():
            return HttpResponse('double')

        if form.is_valid():
            form = form.save(commit=False)
            form.question_id = pk

            if request.user.is_authenticated:
                form.user_id = request.user.id

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.save()
            if not request.user.is_authenticated:
                # Создаем имя пользователя в сессии
                if request.session.get('quest_name') is None:
                    request.session['quest_name'] = request.POST.get('name')
                # Создаем Email пользователя в сессии
                if request.session.get('quest_email') is None:
                    request.session['quest_email'] = request.POST.get('email')
                # Переопределяем пользователя в сессии
                if request.session.get('quest_name') != request.POST.get('name'):
                    request.session['quest_name'] = request.POST.get('name')
                if request.session.get('quest_email') != request.POST.get('email'):
                    request.session['quest_email'] = request.POST.get('email')

            return HttpResponse('success')


class AddQuestion(View):
    """Создание вопроса"""
    def post(self, request):
        form = QuestionForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.author_id = request.user.id
            form.save()
            return HttpResponse('success')

        return HttpResponse('error')
