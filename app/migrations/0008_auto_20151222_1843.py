# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20151215_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.ImageField(upload_to=b'profile'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details_file',
            field=models.FileField(null=True, upload_to=b'tech_det', blank=True),
        ),
    ]
