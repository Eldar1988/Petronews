from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from publications.models import Publication

from .models import Author
from .forms import AvatarForm, BgForm, PublicationForm


class RegisterUser(View):
    def get(self, request):
        return render(request, 'profiles/register.html')

    def post(self, request):
        new_user_name = request.POST.get('username')
        new_user_password = request.POST.get('password')
        user_password_confirm = request.POST.get('password_confirmation')

        if new_user_password != user_password_confirm:
            message = 'Пароли не совпадают, попробуйте еще раз.'
            return render(request, 'profiles/register.html', {'message': message})

        user_already_exists = authenticate(username=new_user_name, password=new_user_password)
        if user_already_exists is not None:
            message = 'Пользователь с таким email уже зарегистрирован.'
            return render(request, 'profiles/register.html', {'message': message})

        new_user = User.objects.create_user(
            username=new_user_name, password=new_user_password, email=new_user_name
        )
        new_user.save()

        profile = Author.objects.create(
            user=new_user
        )
        profile.save()

        return redirect('login')


class ProfileView(View):
    """Профиль пользователя"""
    def get(self, request, pk):
        profile = Author.objects.get(id=pk)
        publications = Publication.objects.filter(author_id=pk)
        success = False
        form = PublicationForm()
        if not request.user.is_anonymous and request.user.author.id == pk:
            success = True
        return render(request, 'profiles/profile.html', {
            'profile': profile,
            'success': success,
            'publications': publications,
            'form': form,
        })


def login_success_view(request):
    return render(request, 'profiles/login_success.html')


class UserNameUpdate(View):
    """Обновление имени автора"""
    def post(self, request, pk):
        profile = Author.objects.get(id=pk)
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.professional = request.POST.get('professional')
        profile.company = request.POST.get('company')
        profile.bio = request.POST.get('bio')
        profile.save()

        return HttpResponse('success')


class UserChangeAvatar(View):
    """Обновление имени автора"""
    def post(self, request, pk):
        profile = Author.objects.get(id=pk)
        form = AvatarForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

        return redirect('profile', pk)


class UserChangeBg(View):
    """Обновление имени автора"""
    def post(self, request, pk):
        profile = Author.objects.get(id=pk)
        form = BgForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            print('sss')

        return redirect('profile', pk)


class AddPublication(View):
    """Создание публикации"""
    def post(self, request, pk):
        form = PublicationForm(request.POST, request.FILES)

        if form.is_valid():
            print('11111')
            form = form.save(commit=False)
            form.author_id = pk
            form.save()
            return redirect('profile', pk)


class EditPublication(View):
    """Редактирование пуликации"""
    def get(self, request, pk):
        publication = Publication.objects.get(id=pk)
        form = PublicationForm(initial={
            'title': publication.title,
            'category': publication.category,
            'body': publication.body,
            'image': publication.image.url
        })

        return render(request, 'profiles/pub_edit_mode.html', {
            'publication': publication,
            'form': form
        })

    def post(self, request, pk):
        publication = Publication.objects.get(id=pk)
        form = PublicationForm(request.POST, request.FILES, instance=publication)

        if form.is_valid():
            form.save()

            return render(request, 'profiles/pub_edit_mode.html', {
                'publication': publication,
                'form': form,
                'success': True
            })

        return render(request, 'profiles/pub_edit_mode.html', {
            'publication': publication,
            'form': form
        })