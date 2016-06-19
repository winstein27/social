# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Profile(models.Model):

    name = models.CharField(max_length=100, blank=False)

    profile_image = models.ImageField(
        upload_to='profile/%Y/%m/%d/', blank=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
