# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm


class FeedView(View):
    template_name = 'feed/feed.html'

    @method_decorator(login_required)
    def get(self, request):
        post_list = Post.objects.all().order_by('-pub_date')

        return render(request, self.template_name, {'post_list': post_list})

    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = Post()
            post.text = form.cleaned_data['text']
            post.image = form.cleaned_data['image']
            post.author = request.user.profile

            post.save()

        return redirect(reverse('feed:feed'))
