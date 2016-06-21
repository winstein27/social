# -*- coding:utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm


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
