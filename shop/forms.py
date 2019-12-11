from django import forms
from .models import Good, Image,Category,Post,Theory,Order


class GoodForm(forms.ModelForm):

    title = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:

        model = Good
        fields = ('title', 'description', 'category', 'price')
        labels = {'title': 'Название',
                  'description': 'Описание',
                  'category': 'Категория',
                  'price': 'Цена',
                  }


class ImageForm(forms.ModelForm):

    image = forms.ImageField(label='Image')

    class Meta:

        model = Image
        fields = ('image', 'good' )


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category
        fields = ('name', 'parent',)
        labels = {'name': 'Название',
                  'parent': 'Надкатегория',
                  }
        values = {"save": 'Добавить'}


class QuantityForm(forms.Form):

    quantity = forms.IntegerField()


class OrderForm(forms.ModelForm):

    class Meta:

        model = Order
        fields = ('user', 'phone', 'city', 'street', 'build', 'aptmt',
                  'payment')
        labels = {'user': 'Имя Фамилия',
                  'phone': 'Телефон',
                  'city': 'Населенный пункт',
                  'street': 'Улица',
                  'build': 'Дом',
                  'aptmt': 'Квартира',
                  'payment': 'Оплата'}
        values = {"save": 'Оформить заказ'}
        widgets = {
            'payment': forms.RadioSelect(choices=[(1, 'Карта Приват'),
                                        (2, 'Наложенным платежом')])}


class TheoryForm(forms.ModelForm):

    class Meta:

        model = Theory
        fields = ('name', 'parent', 'text')
        labels = {'name': 'Тема',
                  'parent': 'Надтема',
                  'text':'Тело',
                  }
        values = {"save": 'Сохранить'}


class PostForm(forms.ModelForm):

    user = forms.CharField(label='Автор')

    class Meta:

        model = Post
        fields = ('post', 'user')
        labels = {'post': 'ИМХО'}
        values = {"save": 'Добавить'}