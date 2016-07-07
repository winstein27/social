# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.test import TestCase

import os

from authentication.models import Profile


class ProfileViewTest(TestCase):

    @staticmethod
    def get_image_path():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return BASE_DIR + '/files/profile_test.jpg'

    @classmethod
    def setUp(cls):
        user = User.objects.create(
            username='test_user',
            password='test_password',
            email='email@test.com',
            first_name='First',
            last_name='Last',
        )

        cls.profile = Profile.objects.create(user=user)

    @classmethod
    def tearDown(cls):
        cls.profile.user.delete()
        cls.profile.delete()

    def access_profile_screen(self):
        self.client.force_login(self.profile.user)
        return self.client.get(reverse('authentication:profile'))

    def try_to_edit_profile(self, context):
        self.client.force_login(self.profile.user)
        return self.client.post(
            reverse('authentication:profile'), context, follow=True)

    def test_profile_details(self):
        """
        Checks if all the profile`s data are displayed
        """
        response = self.access_profile_screen()

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
                'username': 'changed_username',
                'password': 'changed_password',
                'email': 'new@email.com',
                'first_name': 'changed_first_name',
                'last_name': 'changed_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertNotContains(response, 'changed_username')
        self.assertNotContains(response, 'changed_password')
        self.assertContains(response, 'new@email.com')
        self.assertContains(response, 'changed_first_name')
        self.assertContains(response, 'changed_last_name')
        self.assertContains(response, 'profile_test')

    def test_edit_profile_without_first_name(self):
        """
        Trying to edit the profile without a first name, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'changed_username',
                'password': 'changed_password',
                'email': 'new@email.com',
                'first_name': '',
                'last_name': 'changed_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'changed_username')
        self.assertNotContains(response, 'changed_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'changed_first_name')
        self.assertNotContains(response, 'changed_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_last_name(self):
        """
        Trying to edit the profile without a last name, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'changed_username',
                'password': 'changed_password',
                'email': 'new@email.com',
                'first_name': 'changed_first_name',
                'last_name': '',
                'image': image,
            }

            response = self.try_to_edit_profile(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'changed_username')
        self.assertNotContains(response, 'changed_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'changed_first_name')
        self.assertNotContains(response, 'changed_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_email(self):
        """
        Trying to edit the profile without an email, the profile
        must not be updated
        """
        response = None

        with open(self.get_image_path(), 'rb') as image:
            context = {
                'username': 'changed_username',
                'password': 'changed_password',
                'email': '',
                'first_name': 'changed_first_name',
                'last_name': 'changed_last_name',
                'image': image,
            }

            response = self.try_to_edit_profile(context)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertNotContains(response, 'changed_username')
        self.assertNotContains(response, 'changed_password')
        self.assertNotContains(response, 'new@email.com')
        self.assertNotContains(response, 'changed_first_name')
        self.assertNotContains(response, 'changed_last_name')
        self.assertNotContains(response, 'profile_test')

    def test_edit_profile_without_image(self):
        """
        Trying to edit the profile without an image, the profile must
        be updated and displayed
        """
        response = None

        context = {
            'username': 'changed_username',
            'password': 'changed_password',
            'email': 'new@email.com',
            'first_name': 'changed_first_name',
            'last_name': 'changed_last_name',
        }

        response = self.try_to_edit_profile(context)
        print(self.profile.image)
        print(response.context['profile'].image)

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertNotContains(response, 'changed_username')
        self.assertNotContains(response, 'changed_password')
        self.assertContains(response, 'new@email.com')
        self.assertContains(response, 'changed_first_name')
        self.assertContains(response, 'changed_last_name')


class ProfilePasswordViewTest(TestCase):

    username = 'test_user'
    password = 'user_password'

    @classmethod
    def setUp(cls):
        cls.user = User()
        cls.user.username = cls.username
        cls.user.set_password(cls.password)
        cls.user.save()

    @classmethod
    def tearDown(cls):
        cls.user.delete()

    def try_to_change_password(self, context):
        self.client.login(username=self.username, password=self.password)
        return self.client.post(reverse('authentication:password'), context)

    def test_change_password_with_wrong_old_password(self):
        """
        Trying to change the password with a wrong old password must not chage
        it
        """
        context = {
            'old_password': 'wrong_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }

        response = self.try_to_change_password(context)

        self.assertEqual(response.status_code, 409)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    def test_change_password_with_different_new_passwords_1_and_2(self):
        """
        Trying to change the password with different new and verification
        password must not change it
        """
        context = {
            'old_password': self.password,
            'new_password1': 'new_password',
            'new_password2': 'verification_password'
        }

        response = self.try_to_change_password(context)

        self.assertEqual(response.status_code, 409)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    def test_change_password_with_correct_values(self):
        """
        Trying to change the password with correct old password and same new
        and verification password must change the user's password and return
        a url to redirect
        """
        new_password = 'new_password'
        context = {
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password
        }

        response = self.try_to_change_password(context)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode(), reverse('authentication:login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
