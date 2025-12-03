from unittest.mock import patch
import os


from django.test import TestCase, Client
from django.urls import reverse




class WeatherViewTests(TestCase):
	def setUp(self):
		self.client = Client()
		# Ensure env var exists for tests
		os.environ.setdefault('OPENWEATHER_API_KEY', 'test-key')

	@patch('main.views.requests.get')
	def test_happy_path(self, mock_get):
		mock_get.return_value.status_code = 200
		mock_get.return_value.json.return_value = {
			'name': 'Bucharest',
			'main': {'temp': 21.2, 'humidity': 50, 'pressure': 1012},
			'weather': [{'description': 'clear sky', 'icon': '01d'}],
		}
		resp = self.client.post(reverse('index'), {'city': 'Bucharest'})
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Bucharest')
		self.assertContains(resp, '21') # rounded display
		self.assertContains(resp, 'clear sky'.capitalize())

	@patch('main.views.requests.get')
	def test_city_not_found(self, mock_get):
		mock_get.return_value.status_code = 404
		resp = self.client.post(reverse('index'), {'city': 'NoWhereVille'})
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'City not found')