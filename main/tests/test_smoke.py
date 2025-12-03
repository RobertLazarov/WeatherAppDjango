from unittest.mock import patch
import os
from django.test import TestCase, Client
from django.urls import reverse

class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        os.environ.setdefault("OPENWEATHER_API_KEY", "test-key")

    def test_index_get_renders(self):
        # requires main/urls.py to define: path('', index, name='index')
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)
