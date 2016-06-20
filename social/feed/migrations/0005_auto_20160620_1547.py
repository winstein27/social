# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20160620_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
            ],
        ),
        migrations.DeleteModel(
            name='Publicacao',
        ),
    ]
