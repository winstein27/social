# -*- coding:utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import ProfileForm, PasswordForm
from .models import Profile


class ProfileView(View):

    @method_decorator(login_required)
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(user=request.user)

        return render(
            request, 'authentication/profile.html', {'profile': profile})

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            if form.cleaned_data['image']:
                user.profile.image = form.cleaned_data['image']
                user.profile.save()

        return redirect(reverse('authentication:profile'))


class ProfilePasswordView(View):

    @method_decorator(login_required)
    def post(self, request):
        form = PasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            verification_password = form.cleaned_data['verification_password']

            if new_password != verification_password:
                return HttpResponse(status=409)

            username = request.user.username
            password = form.cleaned_data['old_password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user.set_password(new_password)
                user.save()

                return HttpResponse(status=200)

        return HttpResponse(status=409)
