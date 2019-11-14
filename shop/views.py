from django.shortcuts import render,redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, GoodForm,CategoryForm,QuantityForm
from .models import Image,Category,Good

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
    cat = request.GET.get('cat')
    form = QuantityForm(initial={'quantity':1})
    goods = Good.objects.filter(category__slug=cat)
    #images = Image.objects.all()

    if len(Category.objects.filter(slug=cat))>0:
        if get_object_or_404(Category, slug=cat).parent != None:

            categories = Category.objects.filter(slug=get_object_or_404(Category, slug=cat).parent.slug)[0].children.all()
        else:
            categories = Category.objects.filter(parent__slug=cat)
        #categories = Category.objects.all()
    else:
        categories = Category.objects.filter(parent=None)
    print (form)
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