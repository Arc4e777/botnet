# Generated by Django 5.0b1 on 2023-12-19 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0006_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='sleep',
        ),
    ]
