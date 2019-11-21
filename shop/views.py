from django.shortcuts import render,redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, GoodForm,CategoryForm,QuantityForm,PostForm,TheoryForm,OrderForm
from .models import Image,Category,Good,Post,Theory,Order,Basket
from django.template import Context, Template
from django.db.models import Sum,F,FloatField
from django import template



def tree(request,a, menu, theme):

    menu = menu + '<ul>'

    for i in a:

        menu = menu + '<li>'
        menu = menu +'<a href="{% url \''+theme+'\' %}?cat='+i.slug+'" >'+i.name+'</a>'

        if i.children.count()>0:
            menu = tree(request,i.children.all(), menu,theme)

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
def good(request):
    good=Good()
    good.save()
    user = request.user
    print(user.id)
    good.user.add(user)
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
            return redirect('goods')

    else:
        goodform = GoodForm(instance=good)


    return render(request, 'core/model_form_upload.html', {'form': goodform,'images':images,'nn':nn})


def goods(request):
    #request.session.flush()
    if request.method == "POST":


        if request.session.get('order') is None:
            order = Order()
            order.save()
            request.session['order']=order.pk

        basket = Basket()
        print(request.POST.get('good'))
        print(request.session.get('order'))
        basket.good = Good.objects.get(pk=request.POST.get('good'))
        basket.order = Order.objects.get(pk=request.session['order'])
        basket.quantity = request.POST.get('quantity')
        basket.save()


    cat = request.GET.get('cat')
    form = QuantityForm(initial={'quantity':1})
    goods = Good.objects.filter(category__slug=cat)
    #images = Image.objects.all()
    categories=Category.objects.filter(parent=None)
    categories = Template(tree(request,categories, '', 'goods')).render(Context())




    return render(request, 'shop/goods.html', {'goods': goods,'categories':categories,'form':form})


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
        del request.session['order']
        request.session.modified = True
        form=OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'ordered'
            order.save()
            return redirect('goods')

    if 'order' in request.session.keys():
        order = get_object_or_404(Order, pk=request.session['order'])
        goods = Basket.objects.filter(order__pk=request.session['order'])
        form = OrderForm()
    else:
        goods = []

    return render(request, 'shop/basket.html', {'goods': goods,'form':form})

def basket_delete(request,nn):
    good = get_object_or_404(Basket, pk=nn)
    good.delete()
    return redirect('basket')


def orders(request):
    orders = Order.objects.all()
    return render(request, 'shop/orders.html', {'orders': orders})









def theory(request):
    theme = request.GET.get('cat')
    themes = Theory.objects.filter(parent=None)
    menu = Template(tree(request,themes,'','theory')).render(Context())
    if theme!='' and theme!=None:
        theme = get_object_or_404(Theory, slug=theme)
        theme=Template(theme.text).render(Context())

    return render(request, 'shop/theory.html', {'theory': theme,'menu':menu})

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
    posts=Post.objects.all()
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





