#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
* Project Name : npupa_bot
* File Name    : weather.py
* Description  : Query weather forecast
* Create Time  : 2020-05-13 11:26:21
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
'''

import json
import requests
import astral
import datetime
import pytz
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from astral.sun import sun
from astral import LocationInfo
from functions import token as tk
from functions import format_string as fs
from functions.message_handler import bot_print


wthr_key = tk.get_weather_key()


class Weather:
    weather_type = ''

    def get_all(self):
        res = fs.format_en(self.__dict__)
        return res
        # return self.__dict__

    def get_coordinate(self):
        lat = str(self.latitude) + ' N' if self.latitude > 0 else ' S'
        lon = str(self.longitude) + ' E' if self.longitude > 0 else ' W'
        return (lat, lon)

    def request(self):
        url = f'https://free-api.heweather.net/s6/weather/{self.weather_type}?location={self.longitude},{self.latitude}&key={wthr_key}'
        self.res_json = requests.get(url).text
        self.res_dict = json.loads(self.res_json)['HeWeather6'][0]
        self.time_zone = 'UTC ' + self.res_dict['basic']['tz']
        self.update_time = self.res_dict['update']['loc']
        self.location = self.res_dict['basic']['location']
        self.city = self.res_dict['basic']['parent_city']
        self.admin_area = self.res_dict['basic']['admin_area']
        self.country = self.res_dict['basic']['cnty']
        self.latitude = self.res_dict['basic']['lat']
        self.longitude = self.res_dict['basic']['lon']

    def __init__(self, location: str = '北京', latitude: float = 39.90498734, longitude: float = 116.4052887):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.lat_str, self.lon_str = self.get_coordinate()
        self.city = ''
        self.admin_area = ''
        self.country = ''
        self.update_time = ''
        self.time_zone = ''
        self.res_json = ''
        self.res_dict = {}


class WeatherNow(Weather):
    weather_type = 'now'

    def request(self):
        Weather.request(self)
        aqi_url = f'https://free-api.heweather.net/s6/air/now?location={self.city}&key={wthr_key}'
        self.aqi_json = requests.get(aqi_url).text
        self.aqi_dict = json.loads(self.aqi_json)['HeWeather6'][0]

    def __init__(self, location: str = '北京', latitude: float = 39.90498734, longitude: float = 116.4052887):
        Weather.__init__(self, location, latitude, longitude)
        self.aqi_json = ''
        self.aqi_dict = {}


class Astronomy(object):
    pass

def run():
    x = WeatherNow(latitude=46.582859, longitude=125.138808)
    x.request()
    print(x.weather_type)
    p = x.get_all()
    print(p)


# latitude = 46.582859
# longitude = 125.138808

# city = LocationInfo(latitude=latitude, longitude=longitude,
#                     timezone='Asia/Shanghai')
# print((
#     f"Information for {city.name}/{city.region}\n"
#     f"Timezone: {city.timezone}\n"
#     f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
# ))


# # obs = astral.Observer(latitude=latitude, longitude=longitude)
# s = astral.sun.sun(city.observer, date=datetime.datetime.now(),
#                    tzinfo=pytz.timezone('Asia/Shanghai'))

# gd_r_begin, gd_r_end = astral.sun.golden_hour(
#     city.observer, direction=astral.SunDirection.RISING, tzinfo=pytz.timezone('Asia/Shanghai'))
# gd_s_begin, gd_s_end = astral.sun.golden_hour(
#     city.observer, direction=astral.SunDirection.SETTING, tzinfo=pytz.timezone('Asia/Shanghai'))

# print((
#     f'Dawn:    {s["dawn"]}\n'
#     f'Sunrise: {s["sunrise"]}\n'
#     f'Noon:    {s["noon"]}\n'
#     f'Sunset:  {s["sunset"]}\n'
#     f'Dusk:    {s["dusk"]}\n'

#     f'Golden Hour Rise:    {str(gd_r_begin), str(gd_r_end)}\n'
#     f'Golden Hour Set:    {str(gd_s_begin), str(gd_s_end)}\n'
#     # f'Blue Hour:    {s["dusk"]}\n'
# ))

# print(astral.SunDirection.RISING)
# print(astral.SunDirection.SETTING)
