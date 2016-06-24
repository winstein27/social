# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import PostForm
from .models import Post


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


class PostDeleteView(View):

    @method_decorator(login_required)
    def post(self, request):
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)

        if post.author.user == request.user:
            post.delete()
            return HttpResponse(status=200)

        return HttpResponse(status=401)
