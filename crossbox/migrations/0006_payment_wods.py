# Generated by Django 3.0.14 on 2022-01-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossbox', '0005_auto_20220115_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='wods',
            field=models.IntegerField(default=0, verbose_name='Wods'),
            preserve_default=False,
        ),
    ]
