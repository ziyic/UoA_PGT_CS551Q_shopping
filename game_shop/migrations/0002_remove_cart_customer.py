# Generated by Django 3.2 on 2021-04-25 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
    ]