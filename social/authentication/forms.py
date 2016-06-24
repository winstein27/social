# -*- coding: utf-8 -*-

from django import forms


class ProfileForm(forms.Form):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)


class PasswordForm(forms.Form):

    old_password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=8)

    new_password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=8)

    verification_password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=8)
