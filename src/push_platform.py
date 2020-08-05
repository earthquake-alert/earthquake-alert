'''
@author: Yuto Watanabe
@version: 1.2.0

Copyright (c) 2020 Earthquake alert
'''
from typing import Any

try:
    from transmission import line, slack, discode, tweet  # pyright: reportMissingImports=false
except ModuleNotFoundError:
    from src.transmission import line, slack, discode, tweet


def platform_type_0(user: Any, element: Any) -> None:
    '''
    Send to each platform.
    Type: 0

    Args:
        user(Any): User config.
        element(Any): The data to send.
    '''
    token = user['token']
    text = element['text']
    platform = int(user['platform'])
    if platform == 1:
        line(token, text, None)
    elif platform == 2:
        channel = user['channel']
        slack(token, channel, text, None)
    elif platform == 3:
        discode(token, text, None)
    elif platform == 4:
        consumer_key = user['consumer_key']
        consumer_secret = user['consumer_secret']
        token_secret = user['token_secret']
        tweet(consumer_key, consumer_secret, token, token_secret, text, None)


def platform_type_1(user: Any, element: Any) -> None:
    '''
    Send to each platform.
    Type: 1

    Args:
        user(Any): User config.
        element(Any): The data to send.
    '''
    token = user['token']
    template_path = element['template_path']
    map_path = element['map_path']
    platform = int(user['platform'])
    if platform == 1:
        line(token, element['explanation'][0], template_path)
        if map_path != []:
            line(token, '震度分布図', map_path)
    elif platform == 2:
        channel = user['channel']
        slack(token, channel, element['explanation'][0], template_path)
        if map_path != []:
            slack(token, channel, '震度分布図', map_path)
    elif platform == 3:
        discode(token, element['explanation'][0], template_path)
        if map_path != []:
            discode(token, '震度分布図', map_path)
    elif platform == 4:
        consumer_key = user['consumer_key']
        consumer_secret = user['consumer_secret']
        token_secret = user['token_secret']
        tweet(consumer_key, consumer_secret, token, token_secret,
              element['explanation'][0], [template_path, map_path])
