# Generated by Django 2.2.3 on 2019-10-29 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191028_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='shop/%Y/%m/%d', verbose_name='Image'),
        ),
    ]