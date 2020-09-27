'''
@author: Yuto Watanabe
@version: 1.2.0

Copyright (c) 2020 Earthquake alert
'''
import os
from typing import List, Optional

import requests
import tweepy
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

    try:
        requests.post(line_access_url, headers=headers, params=payload, files=files)
    except requests.exceptions.RequestException as error:
        print(error)


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

    try:
        requests.post(url=slack_access_url, params=param, files=files)
    except requests.exceptions.RequestException as error:
        print(error)


def discode(token: str, text: str, image_path: Optional[str]) -> None:
    '''
    Send information to discode.
    If there is an image path, it will be sent with the image.

    Args:
        token (str): discode webhook.
        text (str): character to send
        image_path (Optional[str]): image path
    '''
    try:
        webhook = DiscordWebhook(url=token, content=text)

        if image_path is not None:
            webhook.add_file(file=open(image_path, 'rb'), filename=os.path.basename(image_path))

        webhook.execute()
    except Exception as error:  # pylint: disable=W0703
        print(error)

# Too many arguments is specifications
# pylint: disable=R0913


def tweet(consumer_key: str, consumer_secret: str, token: str,
          token_secret: str, text: str, image_path: Optional[List[str]]):
    '''
    Tweet on Twitter.
    If there is an image path, we will tweet with the image.

    Args:
        consumer_key (str): consumer key
        consumer_secret (str): consumer secret
        token (str): token
        token_secret (str): token secret
        text (str): Content to send.
        image_path (Optional[List[str]]): The image to send. Up to 4
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    if image_path is None:
        api.update_status(text)
    else:
        if image_path[1] == '':
            api.update_with_media(filename=image_path[0], status=text)
        else:
            status = api.update_with_media(filename=image_path[1], status=text)

            api.update_with_media(filename=image_path[0],
                                  auto_populate_reply_metadata=True, in_reply_to_status_id=status.id)
