# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
# import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20151215_0640'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='listing',
        #     name=b'cropping',
        #     field=image_cropping.fields.ImageRatioField(b'image', '430x360', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
        # ),
        # migrations.AlterField(
        #     model_name='listing',
        #     name='profile_pic',
        #     field=image_cropping.fields.ImageCropField(upload_to=b'profile', blank=True),
        # ),
        migrations.AlterField(
            model_name='listing',
            name='tech_details_file',
            field=models.FileField(null=True, upload_to=b'tech_det', blank=True),
        ),
    ]
