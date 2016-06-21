# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Profile(models.Model):

    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        null=False
    )

    @property
    def first_name(self):
        return self.user.first_name
