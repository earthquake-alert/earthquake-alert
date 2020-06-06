'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import json

from src.python.convert_areas import convert


def test_convert():
    db_file_path = 'src/external/area-code-database/src/areas.db'
    image_file_path = 'src/cache'
    earthquake = json_read('test/example/1.json')

    output = convert(earthquake, db_file_path, image_file_path)

    print(output)


def json_read(json_file_path: str):
    with open(json_file_path, mode='r') as contents:
        json_body = json.load(contents)

    return json_body
