# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arkivo_app', '0012_auto_20170921_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveySection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('order', models.IntegerField()),
                ('survey_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arkivo_app.SurveyTemplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='questioncategory',
            name='parent_category',
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='arkivo_app.SurveySection'),
            preserve_default=False,
        ),
    ]
