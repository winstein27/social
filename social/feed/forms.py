# -*- coding: utf-8 -*-

from django import forms


class PublicacaoForm(forms.Form):

    texto = forms.CharField(widget=forms.Textarea, required=True)
    imagem = forms.ImageField(required=False)
