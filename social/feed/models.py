# -*- coding: utf-8 -*-

from django.db import models


class Post(models.Model):

    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(
        auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
