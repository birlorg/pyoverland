import httpx
import pprint
import pydantic
from typing import List, Optional, Union
import datetime


class LocationProperties(pydantic.BaseModel):
    """
    'properties': {'@id': 'https://api.weather.gov/points/43.9445,-121.3761',
                           '@type': 'wx:Point',
                           'county': 'https://api.weather.gov/zones/county/ORC017',
                           'cwa': 'PDT',
                           'fireWeatherZone': 'https://api.weather.gov/zones/fire/ORZ611',
                           'forecast': 'https://api.weather.gov/gridpoints/PDT/31,35/forecast',
                           'forecastGridData': 'https://api.weather.gov/gridpoints/PDT/31,35',
                           'forecastHourly': 'https://api.weather.gov/gridpoints/PDT/31,35/forecast/hourly',
                           'forecastOffice': 'https://api.weather.gov/offices/PDT',
                           'forecastZone': 'https://api.weather.gov/zones/forecast/ORZ509',
                           'gridId': 'PDT',
                           'gridX': 31,
                           'gridY': 35,
                           'observationStations': 'https://api.weather.gov/gridpoints/PDT/31,35/stations',
                           'radarStation': 'KRTX',
                           'relativeLocation': {'geometry': {'coordinates': [-121.359101,
                                                                                                                             43.987447],
                                                                                             'type': 'Point'},
                                                                    'properties': {'bearing': {'unitCode': 'wmoUnit:degree_(angle)',
                                                                                                                           'value': 195},
                                                                                                   'city': 'Deschutes River '
                                                                                                                   'Woods',
                                                                                                   'distance': {'unitCode': 'wmoUnit:m',
                                                                                                                            'value': 4965.5069065158},
                                                                                                   'state': 'OR'},
                                                                    'type': 'Feature'},
                           'timeZone': 'America/Los_Angeles'},
    """

    id: pydantic.HttpUrl = pydantic.Field(alias="@id")
    type: str = pydantic.Field(alias="@type")
    county: pydantic.HttpUrl
    cwa: str
    fireWeatherZone: pydantic.HttpUrl
    forecast: pydantic.HttpUrl
    forecastGridData: pydantic.HttpUrl
    forecastHourly: pydantic.HttpUrl
    forecastOffice: pydantic.HttpUrl
    forecastZone: pydantic.HttpUrl
    gridId: str
    gridX: int
    gridY: int
    observationStations: pydantic.HttpUrl
    radarStation: str
    relativeLocation: dict
    timeZone: str


class Location(pydantic.BaseModel):
    context: List[Union[str, dict]] = pydantic.Field(alias="@context")
    geometry: dict
    id: pydantic.HttpUrl
    properties: LocationProperties
    type: str

    class Config:
        arbitrary_types_allowed = True


class ForecastPeriods(pydantic.BaseModel):
    """from: ForeCastProperties.periods"""

    detailedForecast: str
    endTime: datetime.datetime
    icon: pydantic.HttpUrl
    isDaytime: bool
    name: str
    number: int
    shortForecast: str
    startTime: datetime.datetime
    temperature: pydantic.conint(lt=120, gt=0)
    temperatureTrend: Union[str, None]
    temperatureUnit: str  # pydantic.constr(max_length=1,regex=r"[FCK]")
    windDirection: str
    windSpeed: str


class ForecastProperties(pydantic.BaseModel):
    """from: Forecast.properties"""

    elevation: dict
    forecastGenerator: str
    generatedAt: datetime.datetime
    periods: List[ForecastPeriods]
    units: str
    updateTime: datetime.datetime
    updated: datetime.datetime
    validTimes: str


class Forecast(pydantic.BaseModel):
    """WeatherGov.forecast_by_location()"""

    context: List[Union[str, dict]] = pydantic.Field(alias="@context")
    geometry: dict
    properties: ForecastProperties
    type: str
    alerts: Union[str,None]


class WeatherGov:
    def __init__(self, email: str, url: str = None):
        """Synchronous API for weather.gov API."""
        self.url = url or "https://api.weather.gov"
        self.headers = {
            "User-Agent": f"pyweathergov, {email}",
        }
        self.client = httpx.Client(base_url=self.url, headers=self.headers, timeout=10)

    def location(self, lat: float, long: float):
        """Get API location given lat/long
        returns Location class
        """
        lat = round(float(lat), 4)
        long = round(float(long), 4)
        r = self.client.get(f"/points/{lat},{long}")
        # return Location(r)
        return Location.parse_raw(r.text)

    def forecast_by_location(self, lat: float, long: float):
        """return Forecast class"""
        loc = self.location(lat, long)
        r = httpx.get(loc.properties.forecast, headers=self.headers)
        return Forecast.parse_raw(r.text)


import asyncio

import aiohttp

import pynws
import atos as sync

USERID = "zie@birl.org"


async def fetch(lat, long):
    d = {}
    async with aiohttp.ClientSession() as session:
        nws = pynws.SimpleNWS(lat, long, USERID, session)
        await nws.set_station()
        await nws.update_observation()
        await nws.update_forecast()
        await nws.update_alerts_forecast_zone()
        d["observation"] = nws.observation
        d["forecast"] = nws.forecast[0]
        d["forecasts"] = nws.forecast
        d["alerts"] = nws.alerts_forecast_zone
        # print(nws.observation)
        # print(nws.forecast[0])
        # print(nws.alerts_forecast_zone)
        return d


def get_weather(lat, long):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch(lat, long))


def async_fetch_weather(lat, long):
    try:
        sync_result = sync.coroutine(fetch(lat, long))
    except:
        return None
    return sync_result


def fetch_weather(lat, long):
    w = WeatherGov(USERID)
    return w.forecast_by_location(lat, long)
