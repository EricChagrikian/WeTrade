# Generated by Django 4.0.5 on 2022-07-29 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppTrading', '0005_alter_trade_amount_alter_trade_close_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]