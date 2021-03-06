from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, GoodForm, CategoryForm, QuantityForm, PostForm,\
    TheoryForm, OrderForm, GalleryForm, GalCatForm
from .models import Image, Category, Good, Post, Theory, Order, Basket,\
    GalCat, Gallery
from django.template import Context, Template
from django.db.models import Sum,F,FloatField
from django import template
from django.core.mail import send_mail


def tree(request,a, menu, theme):
    menu = menu + '<ul>'
    for i in a:
        menu = menu + '<li>'
        menu = menu + '<a href="{% url \'' + theme + '\' %}?cat=' + i.slug +\
               '" >' + i.name + '</a>'
        if i.children.count() > 0:
            menu = tree(request, i.children.all(), menu, theme)
        menu = menu + '</li>'
    menu = menu + '</ul>'
    return menu


#@login_required
def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.save()
            form.save_m2m()
            return redirect('goods')
    else:
        form = CategoryForm()
    return render(request, 'core/category.html', {'form': form})


def goodold(request):
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GoodForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })


@login_required
def good_new(request):
    good=Good()
    good.save()
    user = request.user
    good.user=user
    good.save()
    #good.save_m2m()
    return redirect('good_edit',nn=good.pk)


def good_delete(request, nn):
    good = get_object_or_404(Good, pk=nn)
    good.delete()
    return redirect('goods')


def good_edit(request, nn):
    good = get_object_or_404(Good, pk=nn)
    images = Image.objects.filter(good__pk=nn)
    if request.method == "POST":
        goodform = GoodForm(request.POST, instance=good)
        if goodform.is_valid():
            good = goodform.save(commit=False)
            good.save()
            return redirect('good_edit',nn=good.pk)
    else:
        goodform = GoodForm(instance=good)
    return render(request, 'core/model_form_upload.html',
                  {'form': goodform, 'images': images, 'nn': nn})


def goods(request):
    #request.session.flush()
    if request.method == "POST":
        if request.session.get('order') is None:
            order = Order()
            order.save()
            request.session['order'] = order.pk
        basket = Basket()
        basket.good = Good.objects.get(pk=request.POST.get('good'))
        basket.order = Order.objects.get(pk=request.session['order'])
        basket.quantity = request.POST.get('quantity')
        basket.save()
    cat = request.GET.get('cat')
    if cat=='':
        cat=None
    form = QuantityForm(initial={'quantity': 1})
    goods = Good.objects.filter(category__slug=cat)

    #images = Image.objects.all()
    categories=Category.objects.filter(parent=None)
    categories = Template(tree(request, categories, '',
                               'goods')).render(Context())
    return render(request, 'shop/goods.html', {'goods': goods,
                                               'categories':categories,
                                               'form':form})


def image_new(request,nn):
    good = get_object_or_404(Good, pk=nn)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('good_edit',nn=nn)
    else:
        form = ImageForm(instance=good)
        form.fields["good"].initial = good
    return render(request, 'core/image_upload.html', {
        'form': form
    })


def image_del(request,nn,pk):
    image = get_object_or_404(Image, pk=pk)
    image.delete()
    return redirect('good_edit', nn=nn)


# Create your views here.
def main(request):
    return render(request,'shop/main.html')


def contacts(request):
    return render(request,'shop/contacts.html')


def basket(request):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=request.session['order'])
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'ordered'
            order.total = Basket.objects.filter(
                order__pk=request.session['order']
                ).aggregate(total=Sum(F('quantity') * F('good__price'),
                output_field=FloatField()))['total']
            order.save()
            del request.session['order']
            request.session.modified = True
            return redirect('goods')
    if 'order' in request.session.keys():
        order = get_object_or_404(Order, pk=request.session['order'])
        goods = Basket.objects.filter(order__pk=request.session['order'])
        form = OrderForm(instance=order)
    else:
        form = []
        goods = []
    return render(request, 'shop/basket.html', {'goods': goods,'form': form})


def basket_delete(request,nn):
    good = get_object_or_404(Basket, pk=nn)
    good.delete()
    return redirect('basket')


def orders(request):
    orders = Order.objects.all()
    return render(request, 'shop/orders.html', {'orders': orders})


def order_edit(request,nn):
    order = get_object_or_404(Order, pk=nn)
    goods = Basket.objects.filter(order__pk=nn)
    request.session['order'] = order.pk
    if request.method == 'POST':
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():

            order = form.save(commit=False)
            order.total = Basket.objects.filter(
                order__pk=nn
                ).aggregate(total=Sum(F('quantity') * F('good__price'),
                output_field=FloatField()))['total']
            order.save()
            return redirect('orders')
    else:
        form = OrderForm(instance=order)

    return render(request, 'shop/order.html', {'goods': goods,'form': form})


def theory(request):
    theme = request.GET.get('cat')
    themes = Theory.objects.filter(parent=None)
    menu = Template(tree(request, themes, '', 'theory')).render(Context())
    if theme!='' and theme is not None:
        theme = get_object_or_404(Theory, slug=theme)
        theme=Template(theme.text).render(Context())
    return render(request, 'shop/theory.html', {'theory': theme,'menu': menu})


def theory_new(request):
    if request.method == 'POST':
        form = TheoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('theory')
    else:
        form = TheoryForm()
    return render(request, 'core/theoryform.html', {
        'form': form
    })


def theory_edit(request, slug):
    theme = get_object_or_404(Theory, slug=slug)
    if request.method == "POST":
        form = TheoryForm(request.POST, instance=theme)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('/theory/?cat='+slug)
    else:
        form = TheoryForm(instance=theme)
    return render(request, 'core/theoryform.html', {'form': form})


def theory_delete(request, slug):
    theme = get_object_or_404(Theory, slug=slug)
    theme.delete()
    return redirect('/theory/?cat=')


def theory_adelete(request, nn):
    theme = get_object_or_404(Theory, pk=nn)
    theme.delete()
    return redirect('/theory/?cat=')


def category_adelete(request, nn):
    theme = get_object_or_404(Category, pk=nn)
    theme.delete()
    return redirect('/goods')


def posts(request):
    posts = Post.objects.all()
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm()
        form.fields["user"].initial = user
    return render(request,'shop/posts.html',{'form':form,'posts':posts})


def post_delete(request, nn):
    post = get_object_or_404(Post, pk=nn)
    post.delete()
    return redirect('posts')


def galcategory(request):
    if request.method == "POST":
        form = GalCatForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.save()
            form.save_m2m()
            return redirect('gallery')
    else:
        form = GalCatForm()
    return render(request, 'core/category.html', {'form': form})

def gallery(request):
    #request.session.flush()
    cat = request.GET.get('cat')
    if cat=='':
        cat=None
    gallery = Gallery.objects.filter(category__slug=cat)

    #images = Image.objects.all()
    categories=Category.objects.filter(parent=None)

    return render(request, 'shop/gallery.html',
                   {'gallery': gallery,
                    'nodes':GalCat.objects.all()})


def gallery_new(request):
    slug = request.GET.get('cat')
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/gallery/?cat=' + slug)
    else:
        form = GalleryForm()
        if slug is not '':
            form.fields["category"].initial = GalCat.objects.get(slug=slug)
    return render(request, 'core/theoryform.html', {
        'form': form
    })


def gallery_edit(request, nn):
    theme = get_object_or_404(Gallery, pk=nn)
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES, instance=theme)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            category = theme.category.slug if theme.category is not None else ''
            return redirect('/gallery/?cat=' + category)
    else:
        form = GalleryForm(instance=theme)
    return render(request, 'core/theoryform.html', {'form': form})


def gallery_delete(request, nn):
    theme = get_object_or_404(Gallery, pk=nn)
    category = theme.category.slug if theme.category is not None else ''
    theme.delete()
    return redirect('/gallery/?cat=' + category)

