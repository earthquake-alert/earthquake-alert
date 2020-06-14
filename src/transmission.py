'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import Optional

import requests

from discord_webhook import DiscordWebhook


def line(token: str, text: str, image_path: Optional[str]) -> None:
    '''
    Send information to LINE notify.
    If there is an image path, it will be sent with the image.

    Args:
        token (str): LINE notify token
        text (str): character to send
        image_path (str): image path
    '''
    line_access_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': text}
    if image_path is None:
        files = None
    else:
        files = {'imageFile': open(image_path, 'rb')}
    requests.post(line_access_url, headers=headers, params=payload, files=files)


def slack(token: str, channel: str, text: str, image_path: Optional[str]) -> None:
    '''
    Send information to slack.
    If there is an image path, it will be sent with the image.

    Args:
        token (str): slack token.
        channel (str): slack channel name.
        text (str): character to send
        image_path (Optional[str]): image path
    '''
    param = {'token': token}

    if image_path is None:
        slack_access_url = 'https://slack.com/api/chat.postMessage'
        param['channel'] = channel
        param['text'] = text

        files = None
    else:
        slack_access_url = 'https://slack.com/api/files.upload'
        param['channels'] = channel
        param['initial_comment'] = text
        param['filename'] = os.path.basename(image_path)

        files = {'file': open(image_path, 'rb')}

    requests.post(url=slack_access_url, params=param, files=files)


def discode(token: str, text: str, image_path: Optional[str]) -> None:
    '''
    Send information to discode.
    If there is an image path, it will be sent with the image.

    Args:
        token (str): discode webhook.
        text (str): character to send
        image_path (Optional[str]): image path
    '''
    webhook = DiscordWebhook(url=token, content=text)

    if image_path is not None:
        webhook.add_file(file=open(image_path, 'rb'), filename=os.path.basename(image_path))

    webhook.execute()
