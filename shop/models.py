from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.models import Group

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.PROTECT)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"



    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(unidecode(self.name))
            while True:
                if Category.objects.filter(slug=slug).count()>0:
                    slug = slug + '-'
                else:
                    self.slug = slug
                    break
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Good(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True,)

    price = models.FloatField(blank=True,null=True,)
    description = models.TextField(blank=True,null=True,)
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name = 'owner',null=True,on_delete=models.CASCADE)
    def __str__(self):
        if self.title!=None:
            return self.title
        else:
            return ''

def get_image_filename(instance, filename):
    title = instance.good.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Image (models.Model):
    good = models.ForeignKey(Good, default=None,on_delete=models.CASCADE,null=True,blank=True,related_name='images')
    image = models.ImageField(upload_to='shop/%Y/%m/%d',
                              verbose_name='Image')


class Order(models.Model):
    owner = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    user = models.CharField(max_length=50, default=None,null=True)
    phone = models.CharField(max_length=15, default=None,null=True)
    city = models.CharField(max_length=50, default=None,null=True)
    street = models.CharField(max_length=50, default=None,null=True)
    build = models.CharField(max_length=15, default=None,null=True)
    aptmt = models.CharField(max_length=15, default=None,null=True,blank=True)
    payment = models.IntegerField( default=None,null=True,blank=True)
    total = models.FloatField(blank=True,null=True,)
    status = models.CharField(max_length=50, default=None,null=True)

class Basket(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    good = models.ForeignKey(Good,on_delete=models.CASCADE)
    quantity = models.IntegerField()




class Theory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.PROTECT)
    text = models.TextField()

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "theory"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(unidecode(self.name))
            while True:
                if Theory.objects.filter(slug=slug).count()>0:
                    slug = slug + '-'
                else:
                    self.slug = slug
                    break
        super(Theory, self).save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])



class Post(models.Model):
    user = models.CharField(max_length=20)
    post = models.TextField()

# Create your models here.
