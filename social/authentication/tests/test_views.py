# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.test import TestCase
from django.contrib.auth.models import User

import os

from authentication.models import Profile


class ProfileViewTest(TestCase):

    @staticmethod
    def access_profile_screen(instance):
        instance.client.force_login(instance.profile.user)
        return instance.client.get(reverse('authentication:profile'))

    @staticmethod
    def try_to_edit_profile(instance, context):
        instance.client.force_login(instance.profile.user)
        return instance.client.post(
            reverse('authentication:profile'), context, follow=True)

    @staticmethod
    def get_image_path():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return BASE_DIR + '/files/profile_test.jpg'

    @classmethod
    def setUp(cls):
        user = User()
        user.username = 'test_user'
        user.password = 'test_password'
        user.email = 'email@test.com'
        user.first_name = 'First'
        user.last_name = 'Last'

        user.save()

        cls.profile = Profile()
        cls.profile.user = user

        cls.profile.save()

    @classmethod
    def tearDown(cls):
        cls.profile.user.delete()
        cls.profile.delete()

    def test_profile_details(self):
        """
        Checks if all the profile`s data are displayed
        """
        response = self.access_profile_screen(self)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'], self.profile)

    def test_edit_profile(self):
        """
        Trying to edit the profile with new attributes, the profile must be
        updated and displayed
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'new_username',
                'password': 'new_password',
                'email': 'new@email.com',
                'first_name': 'new_first_name',
                'last_name': 'new_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(self, context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertNotContains(response, 'new_username')
        self.assertNotContains(response, 'new_password')
        self.assertContains(response, 'new@email.com')
        self.assertContains(response, 'new_first_name')
        self.assertContains(response, 'new_last_name')
        self.assertContains(response, 'profile_test')

    def test_edit_profile_without_first_name(self):
        """
        Trying to edit the profile without a first name, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'new_username',
                'password': 'new_password',
                'email': 'new@email.com',
                'first_name': '',
                'last_name': 'new_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(self, context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'new_username')
        self.assertNotContains(response, 'new_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'new_first_name')
        self.assertNotContains(response, 'new_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_last_name(self):
        """
        Trying to edit the profile without a last name, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'new_username',
                'password': 'new_password',
                'email': 'new@email.com',
                'first_name': 'new_first_name',
                'last_name': '',
                'image': image,
            }

            response = self.try_to_edit_profile(self, context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'new_username')
        self.assertNotContains(response, 'new_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'new_first_name')
        self.assertNotContains(response, 'new_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_email(self):
        """
        Trying to edit the profile without an email, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'new_username',
                'password': 'new_password',
                'email': '',
                'first_name': 'new_first_name',
                'last_name': 'new_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(self, context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'new_username')
        self.assertNotContains(response, 'new_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'new_first_name')
        self.assertNotContains(response, 'new_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_image(self):
        """
        Trying to edit the profile without an image, the profile must
        be updated and displayed
        """
        response = None

        context = {
            'username': 'new_username',
            'password': 'new_password',
            'email': 'new@email.com',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
        }

        response = self.try_to_edit_profile(self, context)
        print(self.profile.image)
        print(response.context['profile'].image)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertNotContains(response, 'new_username')
        self.assertNotContains(response, 'new_password')
        self.assertContains(response, 'new@email.com')
        self.assertContains(response, 'new_first_name')
        self.assertContains(response, 'new_last_name')
