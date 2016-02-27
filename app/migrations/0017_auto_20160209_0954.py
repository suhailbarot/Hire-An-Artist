# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20160116_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='rscore',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bio',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
