# Generated by Django 3.0.14 on 2022-01-15 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crossbox', '0003_auto_20210501_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(verbose_name='Día y hora')),
                ('payed_amount', models.IntegerField(verbose_name='Precio pagado')),
                ('stripe_error', models.BooleanField(default=False, verbose_name='Error al pagar en Stripe')),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crossbox.Fee')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crossbox.Subscriber')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
    ]
