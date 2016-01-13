# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20160113_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='fees',
            field=models.IntegerField(verbose_name=b'What are your charges? *', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=app.models.get_file_path, verbose_name=b'Upload your listing picture', blank=True),
        ),
    ]
