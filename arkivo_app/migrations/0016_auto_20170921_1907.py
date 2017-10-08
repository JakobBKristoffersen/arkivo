# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0015_remove_question_section'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questioncategory',
            old_name='section',
            new_name='survey_section',
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='show',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
