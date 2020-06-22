'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
from src.push_platform import platform_type_1


def test_tweet():
    user = {
        "platform": 4,
        "consumer_key": "",
        "consumer_secret": "",
        "token_secret": "",
        "token": "",
        "seismic_intensity": "0",
        "areas": [],
        "is_quick_report": False
    }

    element = {
        "title": "テスト送信",
        "max_seismic_intensity": "5-",
        "explanation": [
            "hogehoge",
            "foo"
        ],
        "epicenter": "hogehoge県",
        "areas": [
            "都道府県",
            "都道府県2"
        ],
        "template_path": "test/images/sample_1.png",
        "map_path": "test/images/sample_1_map.png",
        "type": 1
    }

    platform_type_1(user, element)
