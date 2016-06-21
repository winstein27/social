# -*- coding: utf-8 -*-

from django import forms


class ProfileForm(forms.Form):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)
