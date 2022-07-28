# Generated by Django 3.2.13 on 2022-07-27 12:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.TextField()),
                ('quantity', models.IntegerField()),
                ('open_price', models.IntegerField(blank=True, null=True)),
                ('close_price', models.IntegerField(blank=True, null=True)),
                ('open_datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('close_datetime', models.DateTimeField(blank=True, null=True)),
                ('open', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
