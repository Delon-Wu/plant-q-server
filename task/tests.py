from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import Task

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.task_data = {
            'plant': '测试植物',
            'is_completed': False,
            'task_type': 'work',
            'duration_type': 'once',
            'remark': '测试备注',
            'interval_days': 0
        }

    def test_create_task(self):
        url = reverse('task-list')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_update_task(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-detail', args=[task.id])
        update_data = self.task_data.copy()
        update_data['plant'] = '新植物'
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['plant'], '新植物')

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, **self.task_data)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 0)
