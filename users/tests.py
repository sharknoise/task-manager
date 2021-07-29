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
