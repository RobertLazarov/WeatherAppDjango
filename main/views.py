from typing import Tuple, Optional, Dict
import os
import requests

from django.shortcuts import render
from django.contrib import messages

from .forms import CityForm
from .models import SearchHistory

OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


def fetch_weather(city: str, units: str = 'metric') -> Tuple[Optional[Dict], Optional[str]]:
	"""Call OpenWeather Current Weather API. Returns (data, error_message)."""
	api_key = os.environ.get('OPENWEATHER_API_KEY')
	if not api_key:
		return None, 'Server configuration error: missing OPENWEATHER_API_KEY.'

	params = {
		'q': city,
		'appid': api_key,
		'units': units,
	}
	try:
		resp = requests.get(OPENWEATHER_URL, params=params, timeout=5)
	except requests.RequestException as exc:
		return None, f'Network error: {exc.__class__.__name__}'

	if resp.status_code == 200:
		try:
			payload = resp.json()
		except ValueError:
			return None, 'Upstream returned invalid JSON.'

		try:
			# Extract essentials
			main = payload['main']
			weather0 = payload['weather'][0]
			city_name = payload.get('name') or city
			data = {
				'city': city_name,
				'temperature': float(main['temp']),
				'humidity': int(main['humidity']),
				'pressure': int(main['pressure']),
				'description': str(weather0['description']).capitalize(),
				'icon': str(weather0['icon']),
			}
			return data, None
		except (KeyError, TypeError, ValueError):
			return None, 'Upstream response missing expected fields.'

	if resp.status_code == 404:
		return None, 'City not found.'
	if resp.status_code == 401:
		return None, 'Invalid API key.'

	return None, f'Upstream error: {resp.status_code}'


def index(request):
	form = CityForm(request.POST or None)
	context = {
		'form': form,
		'recent': SearchHistory.objects.order_by('-searched_at', '-id')[:5],
	}

	if request.method == 'POST' and form.is_valid():
		city = form.cleaned_data['city'].strip()
		if not city:
			messages.error(request, 'Please enter a city name.')
			return render(request, 'main/index.html', context)

		weather, error = fetch_weather(city)
		if error:
			messages.error(request, error)
		else:
			# Persist and update context
			SearchHistory.objects.create(
				city_name=weather['city'],
				temperature=weather['temperature'],
				humidity=weather['humidity'],
				pressure=weather['pressure'],
				description=weather['description'],
			)
			context['recent'] = SearchHistory.objects.order_by('-searched_at', '-id')[:5]

			context['weather'] = weather

	return render(request, 'main/index.html', context)