# Generated by Django 2.2.3 on 2019-11-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20191114_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]
