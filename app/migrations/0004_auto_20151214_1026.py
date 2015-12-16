# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=models.URLField(),
        ),
    ]
