# Generated by Django 5.0b1 on 2023-12-14 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_delete_userbotupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbot',
            name='tg_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='TG ID'),
        ),
    ]
