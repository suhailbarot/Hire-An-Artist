# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import awesome_avatar.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20151223_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='profile_pic',
            field=awesome_avatar.fields.AvatarField(upload_to=b'profile'),
        ),
        migrations.RemoveField(
            model_name='listing',
            name='talents',
        ),
        migrations.AddField(
            model_name='listing',
            name='talents',
            field=models.ForeignKey(default=2, to='app.Talent'),
            preserve_default=False,
        ),
    ]
