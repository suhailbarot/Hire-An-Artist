# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20160113_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='fees',
            field=models.IntegerField(verbose_name=b'What are your charges? *'),
        ),
    ]
