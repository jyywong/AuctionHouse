# Generated by Django 3.1.3 on 2021-01-07 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0014_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
