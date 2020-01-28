# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from learning_logs.models import Topic

class TopicViewsTest(TestCase):
    fixtures = ['users.json', 'topics.json']

    def test_login_required(self):
        """
        If the user is not logged in, a redirect is expected
        to login page
        """

        response = self.client.get(reverse('learning_logs:topics'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/?next=/topics/')

    def test_with_empty_topics(self):
        """
        If the user is logged in but doesn't have topics, it should return an empty page
        """

        self.client.login(username='test_basic_user', password='123123123+Ja')
        response = self.client.get(reverse('learning_logs:topics'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.context['topics']))

    def test_with_topics(self):
        """
        If the user is logged and has topics associated, it should return an array with this information
        """

        self.client.login(username='test_complete_user', password='123123123+Ja')
        response = self.client.get(reverse('learning_logs:topics'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Topic.objects.filter(owner_id = 2).count(), len(response.context['topics']))
