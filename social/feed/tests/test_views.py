# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.test import TestCase

import os

from authentication.models import Profile
from feed.models import Post, Comment, Like


class FeedViewTest(TestCase):

    @staticmethod
    def get_image_path():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return BASE_DIR + '/files/image_test.png'

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(
            username='temporary',
            email='temporary@gmail.com',
            password='tempo1234')

        Profile.objects.create(user=cls.user)

    @classmethod
    def tearDown(cls):
        cls.user.delete()

    def create_post(self, text):
        return Post.objects.create(author=self.user.profile, text=text)

    def access_feed(self):
        self.client.force_login(user=self.user)
        return self.client.get(reverse('feed:feed'))

    def try_to_publish(self, context):
        self.client.force_login(user=self.user)
        return self.client.post(reverse('feed:feed'), context, follow=True)

    def test_feed_without_posts(self):
        """
        A warning message must be displayed when there are no posts
        """
        response = self.access_feed()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma publicação')
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_feed_with_one_post(self):
        """
        If there is only one post, it must be displayed on the feed
        without any warning messages
        """
        post = self.create_post('Test Post')

        response = self.access_feed()

        self.assertContains(response, post.text)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['post_list']), 1)

    def test_feed_with_two_posts(self):
        """
        If there are more than one posts, they must be displayed on the
        without any warning messages
        """
        first_post = self.create_post('First Post')
        seconde_post = self.create_post('Second Post')

        response = self.access_feed()

        self.assertContains(response, first_post.text)
        self.assertContains(response, seconde_post.text)
        self.assertNotContains(response, 'Nenhuma publicação')
        self.assertEqual(len(response.context['post_list']), 2)

    def test_publish_with_no_text_and_no_image(self):
        """
        Trying to pusblish a post with no text and no image, the post
        must not be published and the feed must not has any post
        """
        response = self.try_to_publish({})

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
            response = self.try_to_publish({'image': image})

        self.assertNotContains(response, 'image_test')
        self.assertQuerysetEqual(response.context['post_list'], [])
        self.assertEqual(len(response.redirect_chain), 1)

    def test_publish_with_text_and_no_image(self):
        """
        Trying to publish a post with text and no image, the post must be
        published and displayed on the feed
        """
        post_text = 'Post text'
        response = self.try_to_publish({'text': post_text})

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
            response = self.try_to_publish(context)

        self.assertContains(response, post_text)
        self.assertContains(response, 'image_test')
        self.assertEqual(len(response.context['post_list']), 1)
        self.assertEqual(len(response.redirect_chain), 1)


class DeleteViewTest(TestCase):

    @staticmethod
    def create_post(text, author_user):
        return Post.objects.create(text=text, author=author_user.profile)

    @classmethod
    def setUp(cls):
        cls.first_user = User.objects.create(
            username='temporary',
            email='temporary@gmail.com',
            password='tempo1234')

        Profile.objects.create(user=cls.first_user)

        cls.second_user = User.objects.create(
            username='second',
            email='second@second.com',
            password='two_password')

        Profile.objects.create(user=cls.second_user)

    @classmethod
    def tearDown(cls):
        cls.first_user.delete()
        cls.second_user.delete()

    def try_to_delete_a_post(self, user, context):
        self.client.force_login(user)
        return self.client.post(reverse('feed:delete'), context)

    def test_delete_without_posts(self):
        """
        Trying to delete a post that does not exists should return
        a 404 not found
        """
        context = {'post_id': 1}
        response = self.try_to_delete_a_post(self.first_user, context)

        self.assertEqual(response.status_code, 404)

    def test_delete_a_not_owned_post(self):
        """
        Trying to delete a post owned by other profile should return
        a 401 unauthorized
        """
        post = self.create_post('Post text', self.first_user)

        context = {'post_id': post.id}
        response = self.try_to_delete_a_post(self.second_user, context)

        self.assertEqual(response.status_code, 401)
        self.assertIn(post, Post.objects.all())

    def test_delete_a_owned_post(self):
        """
        Trying to delete a owned post must delete the post
        """
        post = self.create_post('Post text', self.first_user)

        context = {'post_id': post.id}
        response = self.try_to_delete_a_post(self.first_user, context)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(post, Post.objects.all())

    def test_delete_a_not_owned_post_among_many_posts(self):
        """
        Trying to delete a post owned by other profile amog many posts
        should return a 401 unauthorized
        """
        post_to_be_deleted = self.create_post(
            'Post to be deleted', self.second_user)

        self.create_post('Post 1', self.first_user)
        self.create_post('Post 2', self.second_user)

        context = {'post_id': post_to_be_deleted.id}
        response = self.try_to_delete_a_post(self.first_user, context)

        post_list = Post.objects.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(post_list.count(), 3)
        self.assertIn(post_to_be_deleted, Post.objects.all())

    def test_delete_a_owned_post_among_many_posts(self):
        """
        Trying to delete a owned amond other posts must delete the post
        """
        post_to_be_deleted = self.create_post('Delete post', self.first_user)

        self.create_post('Post 1', self.first_user)
        self.create_post('Post 2', self.second_user)

        context = {'post_id': post_to_be_deleted.id}
        response = self.try_to_delete_a_post(self.first_user, context)

        post_list = Post.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_list.count(), 2)
        self.assertNotIn(post_to_be_deleted, Post.objects.all())


class CommentViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(
            username='test_user', password='password')
        profile = Profile.objects.create(user=cls.user)
        cls.post = Post.objects.create(text='Post text', author=profile)

    @classmethod
    def tearDown(cls):
        cls.post.delete()
        cls.user.delete()

    def comment_post(self, context):
        self.client.force_login(self.user)
        return self.client.post(
            reverse('feed:add_comment'), context, follow=True)

    def test_create_comment_without_text(self):
        """
        Trying to create a comment without text must not create it
        and redirect to feed screen
        """
        context = {'text': '', 'post': self.post.id}
        response = self.comment_post(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_create_comment_without_post(self):
        """
        Trying to create a comment without post must not create it
        and redirect to feed screen
        """
        context = {'text': 'Comment text', 'post': ''}
        response = self.comment_post(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_create_comment(self):
        """
        Trying to create a comment with text and post must create it
        and redirect to feed screen
        """
        text = 'Comment text'
        context = {'text': text, 'post': self.post.id}
        response = self.comment_post(context)

        created_comment = Comment.objects.get(text=text)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(self.post.comments.all()[0], created_comment)
        self.assertEqual(created_comment.author, self.user.profile)
        self.assertEqual(text, created_comment.text)


class CommentDeleteViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.first_user = User.objects.create(
            username='first_user', password='password')
        first_profile = Profile.objects.create(user=cls.first_user)

        cls.second_user = User.objects.create(
            username='second_user', password='password')
        cls.second_profile = Profile.objects.create(user=cls.second_user)

        cls.post = Post.objects.create(text='Post text', author=first_profile)
        cls.comment = Comment.objects.create(
            text='Comment text', post=cls.post, author=first_profile)

    @classmethod
    def tearDown(cls):
        cls.comment.delete()
        cls.post.delete()
        cls.first_user.delete()
        cls.second_user.delete()

    def delete_comment(self, context, user):
        self.client.force_login(user)
        return self.client.post(reverse('feed:delete_comment'), context)

    def test_delete_comment_with_invalid_id(self):
        """
        Trying to delete a comment with an invalid id must not delete it and
        return a 404 not found
        """
        context = {'comment_id': 0}
        response = self.delete_comment(context, self.first_user)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_delete_comment_not_owned(self):
        """
        Trying to delete a comment not owned must not delete it and
        return a 401 unauthorized
        """
        context = {'comment_id': self.comment.id}
        response = self.delete_comment(context, self.second_user)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_delete_a_owned_comment(self):
        """
        Trying to delete a owned comment must delete it and
        return a 200 ok
        """
        context = {'comment_id': self.comment.id}
        response = self.delete_comment(context, self.first_user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), 0)


class LikeViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.first_user = User.objects.create(
            username='first_user', password='password')
        first_profile = Profile.objects.create(user=cls.first_user)

        cls.second_user = User.objects.create(
            username='second_user', password='password')
        cls.second_profile = Profile.objects.create(user=cls.second_user)

        cls.post = Post.objects.create(text='Post text', author=first_profile)

    @classmethod
    def tearDown(cls):
        cls.post.delete()
        cls.first_user.delete()
        cls.second_user.delete()

    def like_post(self, user, context):
        self.client.force_login(user)
        return self.client.post(reverse('feed:like'), context)

    def test_like_a_nonexistent_post(self):
        """
        Trying to like a nonexistent post must return a 404 not found
        """
        context = {'post_id': 0}
        response = self.like_post(self.first_user, context)

        self.assertEqual(response.status_code, 404)
        self.assertQuerysetEqual(Like.objects.all(), [])

    def test_like_a_post_with_zero_likes(self):
        """
        Trying to like a post that was not liked yet, must return a 200 OK
        and the post's number of likes. A Like object must be created.
        """
        context = {'post_id': self.post.id}
        response = self.like_post(self.first_user, context)

        like = Like.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 1)
        self.assertEqual(like.author, self.first_user.profile)
        self.assertEqual(like.post, self.post)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(int(response.content), 1)

    def test_unlike_a_post(self):
        """
        Trying to unlike a post that was alrealdy liked, must return a 200 OK
        and the post's number of likes. The Like object must be deleted.
        """
        Like.objects.create(author=self.first_user.profile, post=self.post)

        context = {'post_id': self.post.id}
        response = self.like_post(self.first_user, context)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 0)
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(int(response.content), 0)

    def test_like_a_post_with_some_likes(self):
        """
        Trying to like a post that was not liked yet, must return a 200 OK
        and the post's number of likes. A Like object must be created.
        """
        Like.objects.create(author=self.second_user.profile, post=self.post)

        context = {'post_id': self.post.id}
        response = self.like_post(self.first_user, context)

        like = Like.objects.get(author=self.first_user.profile)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 2)
        self.assertEqual(like.author, self.first_user.profile)
        self.assertEqual(like.post, self.post)
        self.assertEqual(self.post.likes.count(), 2)
        self.assertEqual(int(response.content), 2)

    def test_unlike_a_post_with_some_likes(self):
        """
        Trying to unlike a post that was alrealdy liked, must return a 200 OK
        and the post's number of likes. The Like object must be deleted.
        """
        Like.objects.create(author=self.first_user.profile, post=self.post)
        Like.objects.create(author=self.second_user.profile, post=self.post)

        context = {'post_id': self.post.id}
        response = self.like_post(self.first_user, context)

        like = Like.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), 1)
        self.assertNotEqual(like.author, self.first_user.profile)
        self.assertEqual(like.post, self.post)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(int(response.content), 1)
