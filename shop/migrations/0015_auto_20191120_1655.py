# Generated by Django 2.2.3 on 2019-11-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_basket_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='aptmt',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='build',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='street',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
