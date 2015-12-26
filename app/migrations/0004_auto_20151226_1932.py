# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151225_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='group_key',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_10',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_2',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_3',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_4',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_5',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_6',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_7',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_8',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='listing',
            name='param_9',
            field=models.IntegerField(default=-1),
        ),
    ]
