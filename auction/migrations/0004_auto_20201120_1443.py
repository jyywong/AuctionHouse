# Generated by Django 3.1.3 on 2020-11-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
