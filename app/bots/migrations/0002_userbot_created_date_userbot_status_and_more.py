# Generated by Django 5.0b1 on 2023-12-14 00:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbot',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userbot',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('deactivated', 'Deactivated'), ('flood_ban', 'Flood ban')], default='active', max_length=50, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='userbot',
            name='unban_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Unban date'),
        ),
        migrations.AddField(
            model_name='userbot',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated date'),
        ),
    ]
