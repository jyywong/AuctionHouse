# Generated by Django 3.1.3 on 2020-12-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0012_auto_20201121_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='quality',
        ),
        migrations.AddField(
            model_name='order',
            name='quality',
            field=models.CharField(choices=[('New', 'New'), ('LUsed', 'Lightly Used'), ('Used', 'Used'), ('Damaged', 'Damaged')], default='Used', max_length=100),
        ),
    ]
