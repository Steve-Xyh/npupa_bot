#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
* File Name    : token.py
* Description  : Get token from files
* Create Time  : 2020-03-13 12:18:29
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
'''

TOKEN_FILE = './token'
WEATHER_KEY = './weather_key'


def get_token():
    '''Get token from files'''
    token = ''
    with open(TOKEN_FILE, 'r') as f:
        token = f.readline().strip()

    return token


def get_weather_key():
    '''Get weather api key from files'''
    token = ''
    with open(WEATHER_KEY, 'r') as f:
        token = f.readline().strip()

    return token
