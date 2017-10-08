# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0004_survey_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='survey_template',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='arkivo_app.SurveyTemplate'),
            preserve_default=False,
        ),
    ]
