'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import json

from src.convert_message import convert_infomation
import xmltodict


def test_infomation():
    xml_fp = '/Users/yuto_w/Downloads/jmaxml_20200525_Samples/32-39_05_12_100831_VXSE53.xml'
    json_fp = 'test/test_cache/output.json'

    with open(xml_fp) as f:
        text_list = f.readlines()

    text = '\n'.join(text_list)

    earthquake = xmltodict.parse(text)

    output = convert_infomation(earthquake)

    with open(json_fp, mode='w') as contents:
        json.dump(output, contents, indent=4, ensure_ascii=False)
