# Generated by Django 5.0b1 on 2023-12-13 22:44

import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/app/web/bots/sessions'), unique=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['session'])], verbose_name='Session')),
            ],
            options={
                'verbose_name': 'Userbot',
                'verbose_name_plural': 'Userbots',
            },
        ),
    ]
