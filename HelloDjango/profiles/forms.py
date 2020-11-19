from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Author
from publications.models import Publication


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('avatar',)


class BgForm(forms.ModelForm):
    """ Изменение фона"""

    class Meta:
        model = Author
        fields = ('background',)


class PublicationForm(forms.ModelForm):
    """Форма создания публикации"""

    class Meta:
        model = Publication
        fields = ('category', 'title', 'image', 'body')

        widgets = {
            'category': forms.Select(
                attrs={
                    'id': 'category-id',
                    'placeholder': 'Выберите категорию',
                    'class': 'form-control'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'id': 'title-p',
                    'required': '',
                    'placeholder': 'Заголовок публикации',
                    'class': 'form-control'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'id': 'image-p',
                    # 'required': '',
                    'class': 'form-control-file',
                    'lang': 'ru'
                }
            ),
            'body': CKEditorWidget(
                attrs={
                    'required': '',
                }
            )
        }

