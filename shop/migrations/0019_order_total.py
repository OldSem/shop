# Generated by Django 2.2.3 on 2019-11-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
