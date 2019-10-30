from django import forms
from .models import Good, Image,Category

class GoodForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Good
        fields = ('title', 'description','category','price',)
        labels = {'title': 'Название', 'description': 'Описание', 'category': 'Категория', 'price': 'Цена',  }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image', 'good' )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)
        labels = {'name': 'Название', 'parent': 'Надкатегория',}
        values = {"save": 'Добавить'}