from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from users.models import UserModel


class UsersTest(TestCase):

    def setUp(self):
        self.tester = UserModel.objects.create_user(
            username='tester',
            password='AAbc123+-=',
        )

    def test_deletion(self):
        self.client.login(username='tester', password='Abc123+-=')
        tester_id = self.tester.id
        self.client.post(reverse('delete', args=str(tester_id)))
        with self.assertRaises(ObjectDoesNotExist):
            self.tester.refresh_from_db()

    def test_permission(self):
        self.client.login(username='tester', password='Abc123+-=')
        response = self.client.post(
            reverse(
                'delete',
                args=str(self.tester.id),
            ),
            follow=True,
        )
        self.assertRedirects(response, '/users/')
        self.assertTrue(
            UserModel.objects.filter(id=self.tester.id).exists(),
        )
