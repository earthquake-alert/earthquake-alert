'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
from src.transmission import line, slack, discord


def test_line():
    token = ''
    text = 'test test'
    image_path = 'asset/chart.dio.png'

    line(token, text, image_path)


def test_slack():
    token = ''
    channel = '#general'
    text = 'test test'
    image_path = 'asset/chart.dio.png'

    slack(token, channel, text, image_path)


def test_slack_text():
    token = ''
    channel = '#general'
    text = 'test test'

    slack(token, channel, text, None)


def test_discord():
    token = ''
    text = 'test test'
    image_path = 'asset/chart.dio.png'

    discord(token, text, image_path)
