# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from authentication.models import Profile
from feed.models import Post, Like


class PostModelTests(TestCase):

    @staticmethod
    def create_post(text, author):
        return Post.objects.create(text=text, author=author)

    @staticmethod
    def like_post(post, author):
        return Like.objects.create(post=post, author=author)

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(
            username='test_user', password='password')
        Profile.objects.create(user=cls.user)

    @classmethod
    def tearDown(cls):
        cls.user.delete()

    def test_get_posts_with_likes_without_posts(self):
        """
        get_posts_with_likes() must return an empty queryset when there
        are no posts on database
        """
        posts = Post.get_posts_with_likes(self.user)

        self.assertQuerysetEqual(posts, [])

    def test_get_posts_with_likes_with_liked_post(self):
        """
        get_posts_with_likes() must return a queryset with the liked and
        not liked posts when there are posts on database
        """
        other_user = User.objects.create(
            username='other_user', password='password')
        Profile.objects.create(user=other_user)

        post = self.create_post('Post text', other_user.profile)
        self.like_post(post, other_user.profile)
        self.like_post(post, self.user.profile)

        posts = Post.get_posts_with_likes(self.user)

        self.assertEqual(posts.count(), 1)
        self.assertTrue(posts[0].liked)

    def test_get_posts_with_likes_withou_liked_post(self):
        """
        get_posts_with_likes() must return a queryset with the liked and
        not liked posts when there are posts on database
        """
        other_user = User.objects.create(
            username='other_user', password='password')
        Profile.objects.create(user=other_user)

        first_post = self.create_post('Post text', other_user.profile)
        self.like_post(first_post, other_user.profile)

        second_post = self.create_post('Post text', self.user.profile)
        self.like_post(second_post, other_user.profile)

        posts = Post.get_posts_with_likes(self.user)

        self.assertEqual(posts.count(), 2)
        self.assertFalse(posts[0].liked)
        self.assertFalse(posts[1].liked)
