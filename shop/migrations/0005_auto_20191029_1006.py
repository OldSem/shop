# Generated by Django 2.2.3 on 2019-10-29 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20191029_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='good',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Good'),
        ),
    ]
