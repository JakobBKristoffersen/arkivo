# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0010_auto_20170920_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='help_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='usercompany',
            name='view_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('company', 'name')]),
        ),
    ]
