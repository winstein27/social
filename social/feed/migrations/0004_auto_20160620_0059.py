# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_publicacao_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacao',
            name='imagem',
            field=models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d/'),
        ),
    ]
