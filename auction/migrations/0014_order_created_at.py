# Generated by Django 3.1.3 on 2021-01-07 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_auto_20201205_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 4, 15, 5, 50, 243378)),
        ),
    ]
