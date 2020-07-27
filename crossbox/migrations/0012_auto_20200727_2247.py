# Generated by Django 3.0.8 on 2020-07-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossbox', '0011_session_session_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='assisted',
        ),
        migrations.AddField(
            model_name='reservation',
            name='refund',
            field=models.BooleanField(default=False, verbose_name='Devolución'),
        ),
    ]
