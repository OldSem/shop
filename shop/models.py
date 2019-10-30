from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode

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
        self.slug = slugify(unidecode(self.name))
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
    user = models.ManyToManyField(User,related_name = 'owner',null=True)
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


# Create your models here.
