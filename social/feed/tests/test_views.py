# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import os

from feed.models import Post
from authentication.models import Profile


class FeedViewTest(TestCase):

    @staticmethod
    def create_post(instance, text):
        return Post.objects.create(author=instance.user.profile, text=text)

    @staticmethod
    def get_image_path():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return BASE_DIR + '/files/image_test.png'

    @staticmethod
    def try_to_publish(instance, context):
        instance.client.force_login(user=instance.user)
        return instance.client.post(reverse('feed:feed'), context, follow=True)

    @staticmethod
    def access_feed(instance):
        instance.client.force_login(user=instance.user)
        return instance.client.get(reverse('feed:feed'))

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(
            username='temporary',
            email='temporary@gmail.com',
            password='tempo1234')

        profile = Profile()
        profile.user = cls.user
        profile.save()

    @classmethod
    def tearDown(cls):
        cls.user.delete()

    def test_feed_without_posts(self):
        """
        A warning message must be displayed when there are no posts
        """
        response = self.access_feed(self)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma publicação')
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_feed_with_one_post(self):
        """
        If there is only one post, it must be displayed on the feed
        without any warning messages
        """
        post = self.create_post(self, 'Test Post')

        response = self.access_feed(self)

        self.assertContains(response, post.text)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['post_list']), 1)

    def test_feed_with_two_posts(self):
        """
        If there are more than one posts, they must be displayed on the
        without any warning messages
        """
        first_post = self.create_post(self, 'First Post')
        seconde_post = self.create_post(self, 'Second Post')

        response = self.access_feed(self)

        self.assertContains(response, first_post.text)
        self.assertContains(response, seconde_post.text)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['post_list']), 2)

    def test_publish_with_no_text_and_no_image(self):
        """
        Trying to pusblish a post with no text and no image, the post
        must not be published and the feed must not has any post
        """
        response = self.try_to_publish(self, {})

        self.assertQuerysetEqual(response.context['post_list'], [])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publish_with_no_text_and_a_image(self):
        """
        Trying to publish a post with no text and a image, the post must not
        be published and the feed must not has any post
        """
        response = None
        with open(self.get_image_path(), 'rb') as image:
            response = self.try_to_publish(self, {'image': image})

        self.assertNotContains(response, 'image_test')
        self.assertQuerysetEqual(response.context['post_list'], [])
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publish_with_text_and_no_image(self):
        """
        Trying to publish a post with text and no image, the post must be
        published and displayed on the feed
        """
        post_text = 'Post text'
        response = self.try_to_publish(self, {'text': post_text})

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, post_text)
        self.assertEqual(len(response.context['post_list']), 1)

    def test_publish_with_text_and_image(self):
        """
        Trying to publish a post with text and image, the post must be
        published and displayed on the feed
        """
        response = None
        post_text = 'Post text'

        with open(self.get_image_path(), 'rb') as image:
            context = {'text': post_text, 'image': image}
            response = self.try_to_publish(self, context)

        self.assertContains(response, post_text)
        self.assertContains(response, 'image_test')
        self.assertEqual(len(response.context['post_list']), 1)
        self.assertEqual(len(response.redirect_chain), 1)
