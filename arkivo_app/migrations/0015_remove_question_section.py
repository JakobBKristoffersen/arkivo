# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 17:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0014_question_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='section',
        ),
    ]