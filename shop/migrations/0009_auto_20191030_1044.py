# Generated by Django 2.2.3 on 2019-10-30 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20191030_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='user',
            field=models.ManyToManyField(null=True, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
