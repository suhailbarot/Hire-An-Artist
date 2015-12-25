# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151225_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='cropped_pic',
        ),
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=app.models.get_file_path, blank=True),
        ),
    ]
