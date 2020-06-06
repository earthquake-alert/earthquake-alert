'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
from src.python.convert_areas import convert


def test_convert():
    db_file_path = 'src/external/area-code-database/src/areas.db'
    image_file_path = 'src/cache'
    earthquake = [
        {
            "title": "test",
            "max_seismic_intensity": "2",
            "magnitude": 5.0,
            "explanation": [
                "aaa",
                "bbb"
            ],
            "epicenter": {
                "name": "foo",
                "lon": 10,
                "lat": 10
            },
            "areas": {
                "震度1": [
                    2121035
                ],
                "震度2": [
                    2120321,
                    2120344
                ]
            }
        }
    ]

    output = convert(earthquake, db_file_path, image_file_path)

    print(output)
