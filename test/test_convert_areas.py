from src.python.convert_areas import convert


def test_convert():
    db_filepath = 'src/external/area-code-database/src/areas.db'
    earthquake = [
        {
            "title": "test",
            "max_seismic_intensity": "2",
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

    assert convert(earthquake, db_filepath) is None
