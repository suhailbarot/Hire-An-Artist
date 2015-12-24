# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_listing_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=b'profile', blank=True),
        ),
    ]
