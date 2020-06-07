'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import json
import os

from src.python.convert_areas import convert


def test_convert():
    db_file_path = 'src/external/area-code-database/src/areas.db'
    image_file_path = 'src/cache'
    output_file_path = os.path.join(image_file_path, 'output.json')
    earthquake = json_read('test/example/2.json')

    output = convert(earthquake, db_file_path, image_file_path)

    json_write(output_file_path, output)


def json_read(json_file_path: str):
    with open(json_file_path, mode='r') as contents:
        json_body = json.load(contents)

    return json_body


def json_write(json_file_path: str, json_body) -> None:
    with open(json_file_path, mode='w') as contents:
        json.dump(json_body, contents, indent=4, ensure_ascii=False)
