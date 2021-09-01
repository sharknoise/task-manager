from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from users.models import UserModel


class LabelsTest(TestCase):

    def setUp(self):
        self.tester = UserModel.objects.create_user(
            username='tester',
            password='Abc123+-=',
        )
        self.test_label = Label.objects.create(
            name='test_label',
            description='Test label.',
            author=self.tester,
        )
        self.client.login(username='tester', password='Abc123+-=')

    def test_create(self):
        response = self.client.post(
            '/labels/create/',
            {'name': 'tested', 'description': 'Test label.'},
            follow=True,
        )
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(
            'tested',
            Label.objects.get(name='tested').name,
        )
        self.assertEqual(
            'Test label.',
            Label.objects.get(name='tested').description,
        )

    def test_update(self):
        self.client.post(
            reverse('label_update', args=str(self.test_label.id)),
            {'name': 'renamed', 'description': 'New description.'},
        )
        self.test_label.refresh_from_db()
        self.assertEqual(self.test_label.name, 'renamed')
        self.assertEqual(
            'New description.',
            Label.objects.get(name='renamed').description,
        )

    def test_delete(self):
        test_label_id = self.test_label.id
        self.client.post(reverse('label_delete', args=str(test_label_id)))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=test_label_id)
