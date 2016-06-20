# -*- coding: utf-8 -*-

from django import forms


class PostForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.ImageField(required=False)
