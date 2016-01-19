# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20160113_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='tech_details_file',
            field=models.FileField(upload_to=b'tech_det', null=True, verbose_name=b'Additional Detail File', blank=True),
        ),
    ]
