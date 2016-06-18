# -*- coding: utf-8 -*-

from django.db import models


class Publicacao(models.Model):

    texto = models.TextField(blank=False)
    data_de_publicacao = models.DateTimeField(
        auto_now=False, auto_now_add=True)
    imagem = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)
