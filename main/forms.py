from django.forms import CharField, FileInput, ModelForm, Select, Textarea, TextInput
from django import forms
from .models import Comment, Publications


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


class CommentForm(ModelForm):
    text = CharField(
        label="",
        widget=Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Добавить комментарий",
                "rows": 1.5,
                "style": "resize:none; width: 75%; margin-top: 130px; margin-left: 80px; border-radius: 30px;",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["text"]


class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)