# Generated by Django 3.0.8 on 2020-08-15 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='stripe_billing_cycle_anchor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Timestamp próximo pago'),
        ),
    ]