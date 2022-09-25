import pytest

import weatherapi

def test_location():
	w = weatherapi.WeatherGov('test@birl.org')
	l = w.location(43.9445,-121.3761)
	assert isinstance(l,weatherapi.Location)
def test_forecast_by_location():
	w = weatherapi.WeatherGov('test@birl.org')
	f = w.forecase_by_location(43.9445,-121.3761)
	assert isinstance(f,weatherapi.Forecast)
