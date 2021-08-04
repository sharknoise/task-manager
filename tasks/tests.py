from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task
from users.models import UserModel


class TasksTest(TestCase):

    def setUp(self):
        self.tester = UserModel.objects.create_user(
            username='tester',
            password='Abc123+-=',
        )
        self.test_status = Status.objects.create(
            name='test_status',
            author=self.tester,
        )
        self.test_task = Task.objects.create(
            name='test_task',
            author=self.tester,
            status=self.test_status,
        )
        self.client.login(username='tester', password='Abc123+-=')

    def test_create(self):
        response = self.client.post(
            '/tasks/create/',
            {
                'name': 'task2',
                'status': self.test_status.id,
                'description': 'second task',
                'executor': '',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(
            'task2',
            Task.objects.get(name='task2').name,
        )

    def test_update(self):
        self.client.post(
            reverse('task_update', args=str(self.test_task.id)),
            {
                'name': 'updated_task',
                'status': self.test_status.id,
                'description': 'updated description',
                'executor': self.tester.id,
            },
        )
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.name, 'updated_task')
        self.assertEqual(self.test_task.status, self.test_status)
        self.assertEqual(self.test_task.description, 'updated description')
        self.assertEqual(self.test_task.executor, self.tester)

    def test_delete(self):
        test_task_id = self.test_status.id
        response = self.client.post(
            reverse('task_delete', args=str(test_task_id)),
            follow=True,
        )
        self.assertRedirects(response, reverse('tasks_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=test_task_id)
