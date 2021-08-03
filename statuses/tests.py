from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import UserModel


class StatusesTest(TestCase):

    def setUp(self):
        self.tester = UserModel.objects.create_user(
            username='tester',
            password='Abc123+-=',
        )
        self.test_status = Status.objects.create(
            name='test_status',
            author=self.tester,
        )
        self.client.login(username='tester', password='Abc123+-=')

    def test_create(self):
        response = self.client.post(
            '/statuses/create/',
            {'name': 'tested'},
            follow=True,
        )
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(
            'tested',
            Status.objects.get(name='tested').name,
        )

    def test_update(self):
        self.client.post(
            reverse('status_update', args=str(self.test_status.id)),
            {'name': 'renamed'},
        )
        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.name, 'renamed')

    def test_delete(self):
        test_status_id = self.test_status.id
        self.client.post(reverse('status_delete', args=str(test_status_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=test_status_id)
