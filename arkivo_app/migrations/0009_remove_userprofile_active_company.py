# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 15:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0008_usercompany_view_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='active_company',
        ),
    ]
