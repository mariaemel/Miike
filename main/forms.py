from django.forms import CharField, FileInput, ModelForm, Select, Textarea, TextInput
from django import forms
from .models import Comment, Publications

from django.core.exceptions import ValidationError
from PIL import Image


class PublicationsForm(ModelForm):
    class Meta:
        model = Publications
        fields = ["image", "title", "cat"]

        widgets = {
            "image": FileInput(
                attrs={
                    "class": "form-control",
                    "style": "width:60%; margin-left:185px; margin-bottom:-20px; margin-top:-70px",
                    "placeholder": "Загрузите изображение",
                    "align": "center",
                }
            ),
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "width:60%; margin-left:185px; margin-bottom:-20px",
                    "placeholder": "Описание"
                }
            ),
            "cat": Select(
                attrs={
                    "class": "form-control",
                    "style": "width:60%; margin-left:185px; margin-bottom:-10px"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PublicationsForm, self).__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Выберите категорию"

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            img = Image.open(image)
            width, height = img.size
            if width / height != 3 / 4:
                raise ValidationError('Изображение должно быть с соотношением сторон 3:4.')

        return image


class CommentForm(ModelForm):
    text = CharField(
        label="",
        widget=Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Добавить комментарий",
                "rows": 1.5,
                "style": "resize:none; width: 75%; margin-top: 75px; margin-left: 80px; border-radius: 30px;",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["text"]


class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)