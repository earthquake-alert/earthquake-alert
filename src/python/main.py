'''
@author: Yuto Watanabe
@version: 1.0.0

Copyright (c) 2020 Earthquake alert
'''
import time

from convert_areas import convert
from json_operation import json_read


def test_convert():
    '''
    TEST
    '''
    db_file_path = 'src/external/area-code-database/src/areas.db'
    image_file_path = 'src/cache'
    earthquake = json_read('test/example/4.json')

    output = convert(earthquake, db_file_path, image_file_path)
    print(output)


if __name__ == "__main__":
    start = time.time()
    test_convert()
    elapsed_time = time.time() - start
    print(f'Time: {elapsed_time}[sec]')
