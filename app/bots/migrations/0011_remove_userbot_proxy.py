# Generated by Django 5.0b1 on 2023-12-29 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0010_userbot_proxy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbot',
            name='proxy',
        ),
    ]
