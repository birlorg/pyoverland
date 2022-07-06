import asyncio

import aiohttp

import pynws
import atos as sync

USERID = "tara@birl.org"


async def fetch(lat,long):
    d = {}
    async with aiohttp.ClientSession() as session:
        nws = pynws.SimpleNWS(lat,long, USERID, session)
        await nws.set_station()
        await nws.update_observation()
        await nws.update_forecast()
        await nws.update_alerts_forecast_zone()
        d['observation'] = nws.observation
        d['forecast'] = nws.forecast[0]
        d['forecasts'] = nws.forecast
        d['alerts'] = nws.alerts_forecast_zone
        #print(nws.observation)
        #print(nws.forecast[0])
        #print(nws.alerts_forecast_zone)
        return d

def get_weather(lat,long):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch(lat,long))

def fetch_weather(lat,long):
    try:
        sync_result = sync.coroutine(fetch(lat,long))
    except aiohttp.client_exceptions.ClientResponseError:
        return None
    return sync_result
