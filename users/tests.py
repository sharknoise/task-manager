from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from users.models import UserModel


class UsersTest(TestCase):

    def setUp(self):
        self.tester = UserModel.objects.create_user(
            username='tester',
            password='Abc123+-=',
        )

    def test_delete(self):
        self.client.login(username='tester', password='Abc123+-=')
        tester_id = self.tester.id
        self.client.post(reverse('delete', args=str(tester_id)))
        with self.assertRaises(ObjectDoesNotExist):
            self.tester.refresh_from_db()

    def test_register(self):
        credentials = {
            'username': 'test_user',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@jonhdoe.com',
            'password1': 'Abc123+-=',
            'password2': 'Abc123+-=',
        }
        response = self.client.post(
            reverse('register'),
            credentials,
            follow=True,
        )
        self.assertRedirects(response, reverse('login'))
        # using __str__ we defined for our custom model in users/models.py
        self.assertEqual(
            str(UserModel.objects.get(username='test_user')),
            'John Doe',
        )

    def test_login(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'tester', 'password': 'Abc123+-='},
            follow=True,
        )
        self.assertTrue(response.context['request'].user.is_authenticated)
        self.assertRedirects(response, '/')

    def test_update(self):
        self.client.login(username='tester', password='Abc123+-=')
        self.client.post(
            reverse('update', args=str(self.tester.id)), {
                'username': 'Тестировщик',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'email': 'ivan@mail.ru',
                'password1': 'Abc123+-=',
                'password2': 'Abc123+-=',
            },
        )
        self.tester.refresh_from_db()
        self.assertEqual(self.tester.username, 'Тестировщик')
        self.assertEqual(self.tester.first_name, 'Иван')
        self.assertEqual(self.tester.last_name, 'Иванов')
        self.assertEqual(self.tester.email, 'ivan@mail.ru')

    def test_guest_permissions_redirect(self):
        response = self.client.post(
            '/users/1/delete/',
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('login') + '?next=/users/1/delete/',
        )

    def test_user_permissions(self):
        self.test_user = UserModel.objects.create_user(
            username='test_user',
            password='testuserpassword',
        )
        self.client.login(username='tester', password='Abc123+-=')
        response = self.client.post(
            reverse('update', args=str(self.test_user.id)), {
                'username': 'renamed_test_user',
                'first_name': 'xyz',
                'last_name': 'xyz',
                'email': 'xyz@xyz.com',
                'password1': 'xyz12345',
                'password2': 'xyz12345',
            },
            follow=True,
        )
        self.assertRedirects(response, '/users/')
        self.assertEqual(self.test_user.username, 'test_user')
        response = self.client.post(
            reverse('delete', args=str(self.test_user.id)),
            follow=True,
        )
        self.assertRedirects(response, '/users/')
        self.assertTrue(
            UserModel.objects.filter(id=self.test_user.id).exists(),
        )
