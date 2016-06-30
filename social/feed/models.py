# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from django.db import models

from authentication.models import Profile


class Post(models.Model):

    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               null=False, related_name='posts')

    @staticmethod
    def get_posts_with_likes(user):
        posts = Post.objects.all().order_by('-pub_date')

        for post in posts:
            try:
                Like.objects.get(post=post, author=user.profile)
                post.liked = True
            except ObjectDoesNotExist:
                post.liked = False

        return posts


class Comment(models.Model):

    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, related_name="comments")
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False)


class Like(models.Model):

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, related_name='likes')
